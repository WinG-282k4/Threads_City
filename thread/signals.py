from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from django.conf import settings
from django.db.models import F

from .models import (
    Like,
    LikeComment,
    Comment,
    Follow,
    Notification,
    Repost,
    RepostComment,
)

# Import Pusher client nếu cần
if settings.USE_PUSHER:
    from .pusher_client import group_send
else:
    # Get channel layer for WebSocket communication khi sử dụng Channels
    channel_layer = get_channel_layer()

# Custom channel_layer.group_send function that works with both Pusher and Channels
def channel_group_send(group_name, message_dict):
    if settings.USE_PUSHER:
        # Sử dụng Pusher
        group_send(group_name, message_dict)
    else:
        # Sử dụng Django Channels
        async_to_sync(channel_layer.group_send)(group_name, message_dict)

# ------------ COUNTER UPDATE SIGNALS ------------

@receiver(post_save, sender=Like)
def increment_thread_likes(sender, instance, created, **kwargs):
    """Increment the thread's likes_count when a Like is created"""
    if created:
        # Tăng likes_count lên 1, cần refreshed_from_db sau khi lưu
        instance.thread.likes_count += 1
        instance.thread.save(update_fields=['likes_count'])

@receiver(post_save, sender=LikeComment)
def increment_comment_likes(sender, instance, created, **kwargs):
    """Increment the comment's likes_count when a LikeComment is created"""
    if created:
        instance.comment.likes_count += 1
        instance.comment.save(update_fields=['likes_count'])

@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    """Increment the thread or parent comment's comment_count when a Comment is created"""
    if created:
        if instance.parent_comment:
            # If it's a reply, update the parent comment's comment_count
            instance.parent_comment.comment_count += 1
            instance.parent_comment.save(update_fields=['comment_count'])
        else:
            # If it's a direct comment on a thread, update the thread's comment_count
            instance.thread.comment_count += 1
            instance.thread.save(update_fields=['comment_count'])

# ------------ WEBSOCKET NOTIFICATION SIGNALS ------------
        
@receiver(post_save, sender=Like)
def notify_like_thread(sender, instance, created, **kwargs):
    """Create notification for like and send WebSocket update."""
    thread = instance.thread
    # 1. Create notification
    if created and not thread.user == instance.user:
        notification = Notification.objects.create(
            user=thread.user,
            type="like_thread",
            content=f"{instance.user.username} likes your thread: {thread.content[:20]}...",
            actioner=instance.user,
        )
        channel_group_send(
            f'user_{thread.user.id}',
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
    # 2. Send WebSocket/Pusher update for like count
    try:
        thread.refresh_from_db()
    except Exception:
        pass
    channel_group_send(
        f'thread_{thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'like_update',
                'thread_id': thread.id,
                'likes_count': thread.likes_count,
                'action': 'like' if created else 'unlike'
            }
        }
    )

@receiver(post_delete, sender=Like)
def decrement_thread_likes(sender, instance, **kwargs):
    """Decrement the thread's likes_count when a Like is deleted"""
    thread = instance.thread
    if thread.likes_count > 0:  # Tránh giá trị âm
        thread.likes_count -= 1
        thread.save(update_fields=['likes_count'])

@receiver(post_delete, sender=Like)
def notify_unlike_thread(sender, instance, **kwargs):
    thread = instance.thread
    try:
        thread.refresh_from_db()
    except Exception:
        pass
    channel_group_send(
        f'thread_{thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'like_update',
                'thread_id': thread.id,
                'likes_count': thread.likes_count,
                'action': 'unlike'
            }
        }
    )

@receiver(post_save, sender=LikeComment)
def notify_like_comment(sender, instance, created, **kwargs):
    comment = instance.comment
    if created and not instance.user == comment.user:
        notification = Notification.objects.create(
            user=comment.user,
            type="like_comment",
            content=f"{instance.user.username} likes your comment: {comment.content[:20]}...",
            actioner=instance.user,
        )
        channel_group_send(
            f'user_{comment.user.id}',
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
    try:
        comment.refresh_from_db()
    except Exception:
        pass
    channel_group_send(
        f'thread_{comment.thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'comment_like_update',
                'thread_id': comment.thread.id,
                'comment_id': comment.id,
                'likes_count': comment.likes_count,
                'action': 'like' if created else 'unlike'
            }
        }
    )

@receiver(post_delete, sender=LikeComment)
def decrement_comment_likes(sender, instance, **kwargs):
    """Decrement the comment's likes_count when a LikeComment is deleted"""
    comment = instance.comment
    if comment.likes_count > 0:  # Tránh giá trị âm
        comment.likes_count -= 1
        comment.save(update_fields=['likes_count'])

@receiver(post_delete, sender=LikeComment)
def notify_unlike_comment(sender, instance, **kwargs):
    comment = instance.comment
    try:
        comment.refresh_from_db()
    except Exception:
        pass
    channel_group_send(
        f'thread_{comment.thread.id}',
        {
            'type': 'like_update',
            'content': {
                'type': 'comment_like_update',
                'thread_id': comment.thread.id,
                'comment_id': comment.id,
                'likes_count': comment.likes_count,
                'action': 'unlike'
            }
        }
    )

# @receiver(post_delete, sender=Comment)
# def notify_delete_comment(sender, instance, **kwargs):
#     """Send WebSocket update when a comment is deleted."""
#     # Handle different cases for direct thread comments and replies
#     if not instance.parent_comment:
#         thread = instance.thread
#         # KHÔNG refresh_from_db vì thread có thể đã bị xóa
#         channel_group_send(
#             f'thread_{thread.id}',
#             {
#                 'type': 'comment_update',
#                 'content': {
#                     'type': 'comment_deleted',
#                     'thread_id': thread.id,
#                     'comment_count': thread.comment_count
#                 }
#             }
#         )
#     else:
#         parent_comment = instance.parent_comment
#         # KHÔNG refresh_from_db vì parent_comment có thể đã bị xóa
#         channel_group_send(
#             f'thread_{instance.thread.id}',
#             {
#                 'type': 'comment_update',
#                 'content': {
#                     'type': 'reply_deleted',
#                     'thread_id': instance.thread.id,
#                     'parent_comment_id': parent_comment.id,
#                     'replies_count': parent_comment.comment_count
#                 }
#             }
#         )

# Các signal còn lại giữ nguyên
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
        
        # Send WebSocket/Pusher update
        channel_group_send(
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
        
        # Send WebSocket/Pusher update
        channel_group_send(
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
        
        # Send WebSocket/Pusher update
        channel_group_send(
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
    
    # Ensure we use fresh data
    if instance.parent_comment:
        try:
            instance.parent_comment.refresh_from_db()
        except Exception:
            pass
        comment_count = instance.parent_comment.comment_count
    else:
        try:
            instance.thread.refresh_from_db()
        except Exception:
            pass
        comment_count = instance.thread.comment_count
        
    # Send WebSocket/Pusher update for comment creation
    message_content = {
        'type': 'new_comment',
        'thread_id': instance.thread.id,
        'comment_id': instance.id,
        'content': instance.content,
        'comment_count': comment_count,
        'is_reply': instance.parent_comment is not None,
        'parent_comment_id': instance.parent_comment.id if instance.parent_comment else None,
        'user_info': {
            'id': instance.user.id,
            'username': instance.user.username,
            'avatar': instance.user.profile.avatar.url if hasattr(instance.user, 'profile') and instance.user.profile.avatar else None
        }
    }
    
    channel_group_send(
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
            
            # Send WebSocket/Pusher update
            channel_group_send(
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
            
            # Send WebSocket/Pusher update
            channel_group_send(
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
