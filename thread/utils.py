from .models import Thread, ThreadImage, Comment, CommentImage
import requests
import os
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
import string
import random
from django.core.mail import send_mail
from django.conf import settings


def create_thread_post(content, user):
    # Check for toxic content
    if check_toxic_content(content):
        # Create notification for the user who posted toxic content
        from .models import Notification
        # Limit content length to avoid database errors
        display_content = content[:15] + "..." if len(content) > 15 else content
        Notification.objects.create(
            user=user,
            type="toxic_content",
            content="Your post violates community standards and has been rejected.",
            actioner=user
        )
        
        # Raise validation error
        raise ValidationError(f"Your post with toxic content has been rejected.")
    
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
        # Limit content length to avoid database errors
        display_content = content[:15] + "..." if len(content) > 15 else content
        Notification.objects.create(
            user=user,
            type="toxic_content",
            content="Your comment violates community standards and has been rejected.",
            actioner=user
        )
        
        # Raise validation error
        raise ValidationError(f"Your comment with toxic content has been rejected.")
    
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


def generate_random_password(length=12):
    """Generate a random password with specified length"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def send_password_reset_email(user_email, new_password):
    """Send email with new password to user"""
    subject = 'Password Reset - Thread Clone'
    message = f'''
    Hello,

    Your password has been reset. Here is your new password:

    {new_password}

    Please login with this password and change it immediately for security reasons.

    Best regards,
    Thread Clone Team
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
