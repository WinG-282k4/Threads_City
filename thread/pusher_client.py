import pusher
import json
from django.conf import settings

# Khởi tạo Pusher client
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

# Hàm gửi tin nhắn giống như channel layer
def group_send(group_name, message):
    """
    Gửi tin nhắn đến một channel group
    Tương tự như channel_layer.group_send trong Django Channels
    """
    # Nếu có trường content, sử dụng trực tiếp nội dung của content
    if 'content' in message:
        # Lấy nội dung từ message['content']
        data = message['content']
        event_name = data.get('type', message.get('type', 'message'))
    else:
        # Sử dụng toàn bộ message
        data = message
        event_name = message.get('type', 'message')
    
    # Sử dụng positional arguments - đây là cách dùng đơn giản và ổn định nhất
    # pusher_client.trigger(channel, event, data)
    pusher_client.trigger(group_name, event_name, data) 