from .models import Thread, ThreadImage, Comment, CommentImage
import requests
import os
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError


def create_thread_post(content, user):
    # Check for toxic content
    if check_toxic_content(content):
        # Create notification for the user who posted toxic content
        from .models import Notification
        Notification.objects.create(
            user=user,
            type="toxic_content",
            content=f"Bài viết của bạn vi phạm tiêu chuẩn cộng đồng và đã bị từ chối",
            actioner=user
        )
        
        # Raise validation error
        raise ValidationError("Bài viết của bạn vi phạm tiêu chuẩn cộng đồng")
    
    thread = Thread(content=content)
    thread.user = user
    thread.save()
    return thread


def create_thread_images(image_list, thread):
    for img in image_list:
        thread_image = ThreadImage(thread=thread, image=img)
        thread_image.save()


def create_cmt(content, user, thread, parent_comment=None):
    # Check for toxic content
    if check_toxic_content(content):
        # Create notification for the user who posted toxic content
        from .models import Notification
        Notification.objects.create(
            user=user,
            type="toxic_content",
            content=f"Bình luận của bạn vi phạm tiêu chuẩn cộng đồng và đã bị từ chối",
            actioner=user
        )
        
        # Raise validation error
        raise ValidationError("Bình luận của bạn vi phạm tiêu chuẩn cộng đồng")
    
    comment = Comment(content=content)
    comment.user = user
    comment.thread = thread
    if parent_comment:
        comment.parent_comment = parent_comment
    comment.save()
    return comment


def create_cmt_images(image_list, comment):
    for img in image_list:
        cmt_img = CommentImage(comment=comment, image=img)
        cmt_img.save()


def success_response(data=None):
    response_data = {
        "status": "success",
        "data": data
    }
    return Response(response_data)


def check_toxic_content(text):
    try:
        response = requests.post(
            # 'http://givoxxs.id.vn/classify',
            os.getenv('TOXIC_CLASSIFIER_URL'),
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/json'
            },
            json={'text': text}
        )
        response.raise_for_status()
        result = response.json()
        return result.get('is_toxic', False)
    except Exception as e:
        print(f"Error checking toxic content: {str(e)}")
        return False
