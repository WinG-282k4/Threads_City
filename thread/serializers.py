from rest_framework import serializers
from .models import Thread, Comment, Like, LikeComment, Repost, RepostComment, Follow, Notification
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at', 
                 'likes_count', 'is_liked', 'replies_count', 'parent_comment_id']

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
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    is_reposted = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'content', 'user', 'created_at', 
                 'comments', 'likes_count', 'is_liked',
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

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followed', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    actioner = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'actioner', 'action', 'created_at', 'is_read'] 