from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers

from .models import (
    Thread,
    Comment,
    Like,
    LikeComment,
    Repost,
    RepostComment,
    Follow,
    Notification,
    ThreadImage,
    CommentImage,
)
from .utils import (
    create_thread_post,
    create_thread_images,
    create_cmt,
    create_cmt_images,
    success_response,
    check_toxic_content,
)
from .serializers import (
    ThreadSerializer, CommentSerializer, FollowSerializer,
    NotificationSerializer, UserSerializer
)


@login_required
def home(request):
    return redirect("thread:feed")


@login_required
def feed(request):
    threads = Thread.objects.all()
    paginator = Paginator(threads, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"threads": page_obj, "following": False}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(request, "thread/partials/_more_feed.html", context)
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/partials/_feed.html", context)
    return render(request, "thread/f_feed.html", context)


@login_required
def following_feed(request):
    following = request.user.following.all()
    # Create a list of user IDs of the users that the authenticated user is following
    following_user_ids = [follow.followed.id for follow in following]

    # Use Q objects to construct an OR query to filter threads
    threads_of_following_users = Thread.objects.filter(
        Q(user__id__in=following_user_ids)
    ).distinct()

    paginator = Paginator(threads_of_following_users, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"threads": page_obj, "following": True}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(request, "thread/partials/_more_feed.html", context)
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/partials/_feed.html", context)
    return render(request, "thread/f_feed.html", context)


@login_required
def create_thread(request):
    if request.method == "POST":
        content_list = request.POST.getlist("content")
        image_count_list = request.POST.getlist("image_count")
        image_list = request.FILES.getlist("thread_images")

        # Ensure thred content and thread images are not both empty.
        if len(content_list[0]) == 0 and int(image_count_list[0]) == 0:
            messages.warning(
                request, "You have to provide some content to create thread."
            )
            return redirect("thread:feed")
        
        try:
            # One unit case, just create a thread
            if len(content_list) == 1:
                # create thread
                thread = create_thread_post(content_list[0], request.user)
                create_thread_images(image_list, thread)
            # Two unit case, create thread and create comment
            if len(content_list) == 2:
                # create thread
                thread = create_thread_post(content_list[0], request.user)
                right = int(image_count_list[0])
                create_thread_images(image_list[:right], thread)
                # create comment
                comment = create_cmt(content_list[1], request.user, thread)
                left = int(image_count_list[0])
                right = left + int(image_count_list[1])
                create_cmt_images(image_list[left:right], comment)
            # More thatn two units, create thread, comment and child cmts
            if len(content_list) > 2:
                # create thread
                thread = create_thread_post(content_list[0], request.user)
                right = int(image_count_list[0])
                create_thread_images(image_list[:right], thread)
                # create parent comment
                comment = create_cmt(content_list[1], request.user, thread)
                left = int(image_count_list[0])
                right = left + int(image_count_list[1])
                create_cmt_images(image_list[left:right], comment)
                # create child comments
                i = 2
                previous_cmt = comment  # Keep track of the previous comment
                while i < len(content_list):
                    child_cmt = create_cmt(
                        content=content_list[i],
                        user=request.user,
                        thread=thread,
                        parent_comment=previous_cmt,  # Use the previous comment as parent
                    )
                    left = 0
                    for j in range(i):
                        left += int(image_count_list[j])
                    right = left + int(image_count_list[i])
                    create_cmt_images(image_list=image_list[left:right], comment=child_cmt)
                    previous_cmt = child_cmt  # Update previous comment for next iteration
                    i += 1

            messages.success(request, "Thread created successfully.")
        except ValidationError as e:
            messages.error(request, str(e))
        
        return redirect("thread:feed")
    else:
        return redirect("thread:feed")


@login_required
def get_thread_form_unit(request):
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "partials/htmx/_thread_form_unit.html")
    return redirect("thread:feed")


@login_required
def get_thread_reply_form(request, id):
    if request.META.get("HTTP_HX_REQUEST"):
        thread = get_object_or_404(Thread, pk=id)
        context = {"thread": thread}
        return render(request, "partials/htmx/_thread_reply_form.html", context)
    return redirect("thread:feed")


@login_required
def get_comment_reply_form(request, id):
    if request.META.get("HTTP_HX_REQUEST"):
        comment = get_object_or_404(Comment, pk=id)
        context = {"comment": comment}
        return render(request, "partials/htmx/_comment_reply_form.html", context)
    return redirect("thread:feed")


@login_required
def get_reply_form_unit(request):
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "partials/htmx/_reply_form_unit.html")
    return redirect("thread:feed")


@login_required
def create_reply(request):
    if request.method == "POST":
        content_list = request.POST.getlist("content")
        image_count_list = request.POST.getlist("image_count")
        image_list = request.FILES.getlist("reply_images")
        thread_id = request.POST.get("thread_id")
        comment_id = request.POST.get("comment_id")

        thread = get_object_or_404(Thread, pk=thread_id)
        parent_comment = None
        if comment_id:
            parent_comment = get_object_or_404(Comment, pk=comment_id)

        # Ensure thred content and thread images are not both empty.
        if len(content_list[0]) == 0 and int(image_count_list[0]) == 0:
            messages.warning(
                request, "You have to provide some content to create reply."
            )
            return redirect("thread:feed")
        
        try:
            # One comment case
            cmt = create_cmt(
                content=content_list[0],
                user=request.user,
                thread=thread,
                parent_comment=parent_comment,
            )
            create_cmt_images(
                image_list=image_list[: int(image_count_list[0])], comment=cmt
            )
            # More than one comment case
            if len(content_list) > 1:
                i = 1
                while i < len(content_list):
                    child_cmt = create_cmt(
                        content=content_list[i],
                        user=request.user,
                        thread=thread,
                        parent_comment=parent_comment,  # Use the same parent_comment for all replies
                    )
                    left = 0
                    for j in range(i):
                        left += int(image_count_list[j])
                    right = left + int(image_count_list[i])
                    create_cmt_images(image_list=image_list[left:right], comment=child_cmt)
                    i += 1

            messages.success(request, "Reply created successfully.")
        except ValidationError as e:
            messages.error(request, str(e))
            
        return redirect("thread:detail", thread_id=thread_id)
    else:
        return redirect("thread:feed")


@login_required
def get_thread(request, username, id):
    thread = get_object_or_404(Thread, pk=id)
    direct_comments = Comment.objects.filter(thread=thread, parent_comment=None)

    paginator = Paginator(direct_comments, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"thread": thread, "direct_comments": page_obj}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(
            request,
            "thread/htmx/partials/_more_comment_section_for_thread_page.html",
            context,
        )
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/thread_page.html", context)
    return render(request, "thread/f_thread_page.html", context)


@login_required
def get_reply(request, username, id):
    comment = get_object_or_404(Comment, pk=id)
    sub_comments = Comment.objects.filter(parent_comment=comment, thread=comment.thread)

    paginator = Paginator(sub_comments, 7)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"comment": comment, "sub_comments": page_obj}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(
            request,
            "thread/htmx/partials/_more_comment_section_for_reply_page.html",
            context,
        )
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/reply_page.html", context)
    return render(request, "thread/f_reply_page.html", context)


@login_required
def like_thread_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        thread = get_object_or_404(Thread, pk=id)
        try:
            like_obj = Like.objects.get(thread=thread, user=request.user)
            like_obj.delete()
        except Like.DoesNotExist:
            Like.objects.create(thread=thread, user=request.user)
        return HttpResponse("Success!")
    return redirect("thread:feed")


@login_required
def like_comment_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        comment = get_object_or_404(Comment, pk=id)
        try:
            like_cmt_obj = LikeComment.objects.get(comment=comment, user=request.user)
            like_cmt_obj.delete()
        except LikeComment.DoesNotExist:
            LikeComment.objects.create(comment=comment, user=request.user)
        return HttpResponse("Success!")
    return redirect("thread:feed")


@login_required
def search(request):
    users = User.objects.all().order_by("-date_joined")

    # Annotate each user with a flag indicating whether the authenticated user is following them
    for user in users:
        user.is_followed_by_authenticated_user = Follow.objects.filter(
            follower=request.user, followed=user
        ).exists()

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)

    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(
            request,
            "thread/htmx/partials/_more_search.html",
            {"page_obj": page_obj},
        )

    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/htmx/search.html", {"page_obj": page_obj})
    return render(request, "thread/f_search.html", {"page_obj": page_obj})


@login_required
def search_query(request):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        q = request.POST.get("search")
        users = User.objects.filter(username__icontains=q).order_by("-date_joined")

        # Annotate each user with a flag indicating whether the authenticated user is following them
        for user in users:
            user.is_followed_by_authenticated_user = Follow.objects.filter(
                follower=request.user, followed=user
            ).exists()

        paginator = Paginator(users, 10)
        page_number = request.GET.get("page") or 1

        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_number = 1
        except EmptyPage:
            page_number = 1

        page_obj = paginator.page(page_number)

        return render(
            request,
            "thread/htmx/partials/_search_query.html",
            {"page_obj": page_obj},
        )
    else:
        return redirect("thread:search")


@login_required
def repost_thread_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        thread = get_object_or_404(Thread, pk=id)
        try:
            repost_obj = Repost.objects.get(thread=thread, user=request.user)
            repost_obj.delete()
            messages.success(request, "Thread repost deleted.")
        except Repost.DoesNotExist:
            Repost.objects.create(thread=thread, user=request.user)
            messages.success(request, "Thread reposted.")
        return render(request, "htmx/partials/_notification_messages.html")
    return redirect("thread:feed")


@login_required
def repost_comment_toggle(request, id):
    if request.method == "POST" and request.META.get("HTTP_HX_REQUEST"):
        comment = get_object_or_404(Comment, pk=id)
        try:
            repost_cmt_obj = RepostComment.objects.get(
                comment=comment, user=request.user
            )
            repost_cmt_obj.delete()
            messages.success(request, "Comment repost deleted.")
        except RepostComment.DoesNotExist:
            RepostComment.objects.create(comment=comment, user=request.user)
            messages.success(request, "Comment reposted.")
        return render(request, "htmx/partials/_notification_messages.html")
    return redirect("thread:feed")


@login_required
def get_thread_likes(request, username, id):
    thread = get_object_or_404(Thread, pk=id)
    likes = Like.objects.filter(thread=thread)
    liked_users = [l.user for l in likes]

    # Annotate each user with a flag indicating whether the authenticated user is following them
    for user in liked_users:
        user.is_followed_by_authenticated_user = Follow.objects.filter(
            follower=request.user, followed=user
        ).exists()

    paginator = Paginator(liked_users, 15)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"liked_users": page_obj, "thread": thread}

    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "htmx/partials/_liked_users_of_threads.html", context)
    return redirect("thread:feed")


@login_required
def get_reply_likes(request, username, id):
    comment = get_object_or_404(Comment, pk=id)
    likes_cmts = LikeComment.objects.filter(comment=comment)
    liked_users = [l.user for l in likes_cmts]

    # Annotate each user with a flag indicating whether the authenticated user is following them
    for user in liked_users:
        user.is_followed_by_authenticated_user = Follow.objects.filter(
            follower=request.user, followed=user
        ).exists()

    paginator = Paginator(liked_users, 15)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    context = {"liked_users": page_obj, "comment": comment}

    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "htmx/partials/_liked_users_of_cmts.html", context)
    return redirect("thread:feed")


@login_required
def notification(request):
    notifications = Notification.objects.filter(user=request.user)

    paginator = Paginator(notifications, 15)
    page_number = request.GET.get("page") or 1

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
    except EmptyPage:
        page_number = 1

    page_obj = paginator.page(page_number)
    # Annotate
    for n in page_obj:
        if Follow.objects.filter(follower=n.user, followed=n.actioner).exists():
            n.user.is_already_following = True
        else:
            n.user.is_already_following = False
        # mark is_read
        n.is_read = True
        n.save()

    context = {"notifications": page_obj}
    if request.META.get("HTTP_HX_REQUEST") and int(page_number) > 1:
        return render(request, "thread/partials/_more_notification.html", context)
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "thread/partials/_notification.html", context)
    return render(request, "thread/f_notification.html", context)


@login_required
def check_reddot(request):
    reddot_exists = Notification.objects.filter(
        user=request.user, is_read=False
    ).exists()
    if reddot_exists:
        return HttpResponse(
            "<span class='reddot'></span>"
        )
    else:
        return HttpResponse("<span></span>")


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """
        Allow unauthenticated access to list and feed actions.
        Require authentication for all other actions.
        """
        if self.action in ['list', 'feed']:
            return []
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        # Check toxic content before creating thread
        content = serializer.validated_data.get('content', '')
        if check_toxic_content(content):
            # Create notification for the user who posted toxic content
            # Limit content length to avoid database errors
            display_content = content[:15] + "..." if len(content) > 15 else content
            Notification.objects.create(
                user=self.request.user,
                type="toxic_content",
                content="Your post violates community standards and has been rejected.",
                actioner=self.request.user
            )
            
            raise serializers.ValidationError({
                'status': 'error',
                'errors': {
                    'content': f"Your post with toxic content has been rejected."
                }
            })
            
        # Create thread if content is safe
        thread = serializer.save(user=self.request.user)
        return thread

    def destroy(self, request, *args, **kwargs):
        thread_id = self.kwargs.get('pk')
        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist:
            return Response(
                {"status": "error", "errors": {"detail": "Thread không tồn tại"}},
                status=status.HTTP_404_NOT_FOUND
            )
        if thread.user != request.user:
            return Response(
                {"status": "error", "errors": {"detail": "You can only delete your own threads"}},
                status=status.HTTP_403_FORBIDDEN
            )
        # Comment.objects.filter(thread=thread).delete()
        thread.delete()
        return Response(
            {"status": "success", "data": {"message": "Thread deleted successfully"}},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def feed(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def following_feed(self, request):
        following = request.user.following.all()
        following_user_ids = [follow.followed.id for follow in following]
        queryset = Thread.objects.filter(user__id__in=following_user_ids)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_threads(self, request):
        """Lấy thread do user tạo"""
        queryset = Thread.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_commented_threads(self, request):
        """Lấy thread mà user đã comment"""
        # Lấy các thread mà user đã comment
        commented_thread_ids = Comment.objects.filter(user=request.user).values_list('thread_id', flat=True).distinct()
        queryset = Thread.objects.filter(id__in=commented_thread_ids).exclude(user=request.user)  # Loại bỏ thread của chính user
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_reposted_threads(self, request):
        """Lấy thread mà user đã repost"""
        queryset = request.user.reposted_threads.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_threads(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(id=user_id)
            # Lấy thread của user
            user_threads = Thread.objects.filter(user=user)
            # Lấy thread đã repost
            reposted_threads = user.reposted_threads.all()
            # Kết hợp và sắp xếp theo thời gian
            queryset = (user_threads | reposted_threads).distinct().order_by('-created_at')
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        thread = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, thread=thread)
        if not created:
            like.delete()
        # Refresh thread instance to get updated likes_count from database
        thread.refresh_from_db()
        return Response({
            'likes_count': thread.likes_count,
            'is_liked': thread.liked_users.filter(id=request.user.id).exists()
        })

    @action(detail=True, methods=['post'])
    def repost(self, request, pk=None):
        thread = self.get_object()
        repost, created = Repost.objects.get_or_create(user=request.user, thread=thread)
        if not created:
            repost.delete()
        return Response({
            'reposts_count': thread.reposted_users.count(),
            'is_reposted': thread.reposted_users.filter(id=request.user.id).exists()
        })


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        thread_id = self.kwargs.get('thread_pk')
        return Comment.objects.filter(thread_id=thread_id, parent_comment=None).order_by('-created_at')

    @action(detail=True, methods=['get'])
    def replies(self, request, thread_pk=None, pk=None):
        comment = self.get_object()
        replies = Comment.objects.filter(parent_comment=comment).order_by('-created_at')
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        thread_id = self.kwargs.get('thread_pk')
        thread = get_object_or_404(Thread, id=thread_id)
        parent_comment_id = self.request.data.get('parent_comment_id')
        parent_comment = None
        if parent_comment_id:
            parent_comment = get_object_or_404(Comment, id=parent_comment_id)
            
        # Check toxic content before creating comment
        content = serializer.validated_data.get('content', '')
        if check_toxic_content(content):
            # Create notification for the user who posted toxic content
            # Limit content length to avoid database errors
            display_content = content[:15] + "..." if len(content) > 15 else content
            Notification.objects.create(
                user=self.request.user,
                type="toxic_content",
                content="Your comment violates community standards and has been rejected.",
                actioner=self.request.user
            )
            
            raise serializers.ValidationError({
                'status': 'error',
                'errors': {
                    'content': f"Your comment with toxic content has been rejected."
                }
            })
            
        serializer.save(user=self.request.user, thread=thread, parent_comment=parent_comment)

    @action(detail=True, methods=['post'])
    def like(self, request, thread_pk=None, pk=None):
        # Look up comment by ID regardless of parent_comment status
        comment = get_object_or_404(Comment, id=pk)
        
        like, created = LikeComment.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            like.delete()
        try:
            comment.refresh_from_db()
        except Comment.DoesNotExist:
            pass
        return Response({
            'likes_count': comment.likes_count,
            'is_liked': comment.liked_users.filter(id=request.user.id).exists()
        })

    @action(detail=True, methods=['post'])
    def repost(self, request, thread_pk=None, pk=None):
        comment = self.get_object()
        repost, created = RepostComment.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            repost.delete()
        return Response({'status': 'success'})


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    @action(detail=False, methods=['get'])
    def following(self, request):
        from accounts.serializers import UserSerializer
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = User.objects.filter(followers__follower=user).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def followers_count(self, request):
        count = Follow.objects.filter(followed=request.user).count()
        return Response({'count': count})
        
    @action(detail=False, methods=['get'])
    def user_follows_count(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            followers_count = Follow.objects.filter(followed=user).count()
            following_count = Follow.objects.filter(follower=user).count()
            
            return Response({
                'followers_count': followers_count,
                'following_count': following_count
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=False, methods=['get'])
    def check_status(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            is_followed = Follow.objects.filter(follower=request.user, followed=user).exists()
            
            return Response({
                'is_followed': is_followed
            })
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def followers(self, request):
        from accounts.serializers import UserSerializer
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        queryset = User.objects.filter(following__followed=user).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = UserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        is_read = self.request.query_params.get('is_read', None)
        
        if is_read is not None:
            is_read = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read)
            
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'count': count})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({
            'status': 'success',
            'id': notification.id
        })

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({
            'status': 'success',
            'message': 'All notifications marked as read'
        })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search', None)
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
            
        return queryset
        
    def get_serializer_class(self):
        if self.action == 'retrieve':  # For GET /api/users/{id}/
            from accounts.serializers import UserDetailSerializer
            return UserDetailSerializer
        return self.serializer_class

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        users = User.objects.filter(username__icontains=query)
        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(users, many=True, context={'request': request})
        return Response(serializer.data)
