from .models import Thread, ThreadImage, Comment, CommentImage
import requests
from rest_framework.response import Response
from rest_framework import status


def create_thread_post(content, user):
    thread = Thread(content=content)
    thread.user = user
    thread.save()
    return thread


def create_thread_images(image_list, thread):
    for img in image_list:
        thread_image = ThreadImage(thread=thread, image=img)
        thread_image.save()


def create_cmt(content, user, thread, parent_comment=None):
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
            'http://4.217.235.17/classify',
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
