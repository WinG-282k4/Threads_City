from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

from .models import (
    Like,
    LikeComment,
    Comment,
    Follow,
    Notification,
    Repost,
    RepostComment,
)

# Get channel layer for WebSocket communication
channel_layer = get_channel_layer()

@receiver(post_delete, sender=Like)
def update_likes_count(sender, instance, **kwargs):
    # Update the likes_count of the related Thread when a Like is deleted
    instance.thread.likes_count = Like.objects.filter(thread=instance.thread).count()
    instance.thread.save()
    
    # Send WebSocket update
    async_to_sync(channel_layer.group_send)(
        f'thread_{instance.thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'like_update',
                'thread_id': instance.thread.id,
                'likes_count': instance.thread.likes_count,
                'action': 'unlike'
            }
        }
    )


@receiver(post_delete, sender=LikeComment)
def update_cmt_likes_count(sender, instance, **kwargs):
    # Update the likes_count of the related comment when a Like is deleted
    instance.comment.likes_count = LikeComment.objects.filter(
        comment=instance.comment
    ).count()
    instance.comment.save()
    
    # Send WebSocket update
    async_to_sync(channel_layer.group_send)(
        f'thread_{instance.comment.thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'comment_like_update',
                'thread_id': instance.comment.thread.id,
                'comment_id': instance.comment.id,
                'likes_count': instance.comment.likes_count,
                'action': 'unlike'
            }
        }
    )


@receiver(post_delete, sender=Comment)
def update_comment_count(sender, instance, **kwargs):
    # Update the comment_count of the related Thread when a parent_comment is deleted
    if not instance.parent_comment:
        instance.thread.comment_count = Comment.objects.filter(
            thread=instance.thread, parent_comment=None
        ).count()
        instance.thread.save()
        
        # Send WebSocket update
        async_to_sync(channel_layer.group_send)(
            f'thread_{instance.thread.id}',
            {
                'type': 'comment_update',
                'content': {
                    'type': 'comment_deleted',
                    'thread_id': instance.thread.id,
                    'comment_count': instance.thread.comment_count
                }
            }
        )
    # Update the comment_count of the parent_comment
    else:
        parent_comment = instance.parent_comment
        parent_comment.comment_count = Comment.objects.filter(
            thread=instance.thread, parent_comment=parent_comment
        ).count()
        parent_comment.save()
        
        # Send WebSocket update
        async_to_sync(channel_layer.group_send)(
            f'thread_{instance.thread.id}',
            {
                'type': 'comment_update',
                'content': {
                    'type': 'reply_deleted',
                    'thread_id': instance.thread.id,
                    'parent_comment_id': parent_comment.id,
                    'replies_count': parent_comment.comment_count
                }
            }
        )


@receiver(post_save, sender=Like)
def create_notification_like_thread(sender, instance, created, **kwargs):
    """Create notification for like."""
    if created and not instance.thread.user == instance.user:
        notification = Notification.objects.create(
            user=instance.thread.user,
            type="like_thread",
            content=f"{instance.user.username} likes your thread: {instance.thread.content[:20]}...",
            actioner=instance.user,
        )
        
        # Send WebSocket update
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.thread.user.id}',
            {
                'type': 'notification_update',
                'content': {
                    'type': 'new_notification',
                    'notification_id': notification.id,
                    'notification_type': 'like_thread',
                    'content': notification.content
                }
            }
        )
    
    # Send WebSocket update for like count
    async_to_sync(channel_layer.group_send)(
        f'thread_{instance.thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'like_update',
                'thread_id': instance.thread.id,
                'likes_count': instance.thread.likes_count,
                'action': 'like' if created else 'unlike'
            }
        }
    )


@receiver(post_save, sender=LikeComment)
def create_notification_like_comment(sender, instance, created, **kwargs):
    """Create notification for likeComment."""
    if created and not instance.user == instance.comment.user:
        notification = Notification.objects.create(
            user=instance.comment.user,
            type="like_comment",
            content=f"{instance.user.username} likes your comment: {instance.comment.content[:20]}...",
            actioner=instance.user,
        )
        
        # Send WebSocket update
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.comment.user.id}',
            {
                'type': 'notification_update',
                'content': {
                    'type': 'new_notification',
                    'notification_id': notification.id,
                    'notification_type': 'like_comment',
                    'content': notification.content
                }
            }
        )
    
    # Send WebSocket update for like count
    async_to_sync(channel_layer.group_send)(
        f'thread_{instance.comment.thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'comment_like_update',
                'thread_id': instance.comment.thread.id,
                'comment_id': instance.comment.id,
                'likes_count': instance.comment.likes_count,
                'action': 'like' if created else 'unlike'
            }
        }
    )


@receiver(post_save, sender=Repost)
def create_notification_repost_thread(sender, instance, created, **kwargs):
    """Create notification for Repost."""
    if created and not instance.user == instance.thread.user:
        notification = Notification.objects.create(
            user=instance.thread.user,
            type="repost_thread",
            content=f"{instance.user.username} reposted your thread: {instance.thread.content[:20]}...",
            actioner=instance.user,
        )
        
        # Send WebSocket update
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.thread.user.id}',
            {
                'type': 'notification_update',
                'content': {
                    'type': 'new_notification',
                    'notification_id': notification.id,
                    'notification_type': 'repost_thread',
                    'content': notification.content
                }
            }
        )


@receiver(post_save, sender=RepostComment)
def create_notification_repost_comment(sender, instance, created, **kwargs):
    """Create notification for RepostComment."""
    if created and not instance.user == instance.comment.user:
        notification = Notification.objects.create(
            user=instance.comment.user,
            type="repost_comment",
            content=f"{instance.user.username} reposted your comment: {instance.comment.content[:20]}...",
            actioner=instance.user,
        )
        
        # Send WebSocket update
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.comment.user.id}',
            {
                'type': 'notification_update',
                'content': {
                    'type': 'new_notification',
                    'notification_id': notification.id,
                    'notification_type': 'repost_comment',
                    'content': notification.content
                }
            }
        )


@receiver(post_save, sender=Follow)
def create_notification_follow(sender, instance, created, **kwargs):
    """Create notification for Follow."""
    if created:
        notification = Notification.objects.create(
            user=instance.followed,
            type="follow",
            content=f"{instance.follower.username} started following you.",
            actioner=instance.follower,
        )
        
        # Send WebSocket update
        async_to_sync(channel_layer.group_send)(
            f'user_{instance.followed.id}',
            {
                'type': 'notification_update',
                'content': {
                    'type': 'new_notification',
                    'notification_id': notification.id,
                    'notification_type': 'follow',
                    'content': notification.content
                }
            }
        )


@receiver(post_save, sender=Comment)
def create_notification_comment(sender, instance, created, **kwargs):
    """Create notification for Comment."""
    if not created:
        return
        
    # Send WebSocket update for comment creation
    message_content = {
        'type': 'new_comment',
        'thread_id': instance.thread.id,
        'comment_id': instance.id,
        'content': instance.content,
        'comment_count': instance.thread.comment_count if not instance.parent_comment else instance.parent_comment.comment_count,
        'is_reply': instance.parent_comment is not None,
        'parent_comment_id': instance.parent_comment.id if instance.parent_comment else None,
        'user_info': {
            'id': instance.user.id,
            'username': instance.user.username,
            'avatar': instance.user.profile.avatar.url if hasattr(instance.user, 'profile') and instance.user.profile.avatar else None
        }
    }
    
    async_to_sync(channel_layer.group_send)(
        f'thread_{instance.thread.id}',
        {
            'type': 'comment_update',
            'content': message_content
        }
    )
    
    if instance.parent_comment:
        if not instance.parent_comment.user == instance.user:
            notification = Notification.objects.create(
                user=instance.parent_comment.user,
                type="comment",
                content=f"{instance.user.username} reply to your comment: {instance.parent_comment.content[:20]}...",
                actioner=instance.user,
            )
            
            # Send WebSocket update
            async_to_sync(channel_layer.group_send)(
                f'user_{instance.parent_comment.user.id}',
                {
                    'type': 'notification_update',
                    'content': {
                        'type': 'new_notification',
                        'notification_id': notification.id,
                        'notification_type': 'comment_reply',
                        'content': notification.content
                    }
                }
            )
    else:
        if not instance.thread.user == instance.user:
            notification = Notification.objects.create(
                user=instance.thread.user,
                type="comment",
                content=f"{instance.user.username} reply to your thread: {instance.thread.content[:20]}...",
                actioner=instance.user,
            )
            
            # Send WebSocket update
            async_to_sync(channel_layer.group_send)(
                f'user_{instance.thread.user.id}',
                {
                    'type': 'notification_update',
                    'content': {
                        'type': 'new_notification',
                        'notification_id': notification.id,
                        'notification_type': 'thread_comment',
                        'content': notification.content
                    }
                }
            )
