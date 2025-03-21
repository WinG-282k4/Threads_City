from rest_framework import serializers
from .models import Thread, Comment, Like, LikeComment, Repost, RepostComment, Follow, Notification, ThreadImage
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer

class ThreadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadImage
        fields = ['id', 'image']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at', 
                 'likes_count', 'is_liked', 'replies_count']

    def get_likes_count(self, obj):
        return obj.likecomment_set.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likecomment_set.filter(user=request.user).exists()
        return False

    def get_replies_count(self, obj):
        return obj.sub_comment.count()

class ThreadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    images = ThreadImageSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    is_reposted = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'content', 'user', 'created_at', 
                 'comments', 'images', 'likes_count', 'is_liked',
                 'reposts_count', 'is_reposted', 'comment_count']

    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_set.filter(user=request.user).exists()
        return False

    def get_reposts_count(self, obj):
        return obj.repost_set.count()

    def get_is_reposted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.repost_set.filter(user=request.user).exists()
        return False

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)
    followed_id = serializers.IntegerField(write_only=True)  # Thêm ID để gửi từ request
    status = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'followed_id', 'created_at', 'status']
        read_only_fields = ['follower', 'followed']

    def get_status(self, obj):
        return "Followed successfully" if obj.id else "Unfollowed successfully"

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        followed_id = validated_data.pop("followed_id", None)
        if not followed_id:
            raise serializers.ValidationError({"followed_id": "This field is required."})

        try:
            followed_user = User.objects.get(id=followed_id)
            # Kiểm tra xem đã follow chưa
            follow_obj = Follow.objects.filter(follower=request.user, followed=followed_user).first()
            if follow_obj:
                # Nếu đã follow thì unfollow
                follow_obj.delete()
                # Return a dummy instance to satisfy the serializer
                return Follow(follower=request.user, followed=followed_user)
            # Nếu chưa follow thì tạo mới
            return Follow.objects.create(follower=request.user, followed=followed_user)
        except User.DoesNotExist:
            raise serializers.ValidationError({"followed_id": "User not found."})

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    actioner = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'actioner', 'content', 'created_at', 'is_read'] 