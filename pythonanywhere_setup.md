# Hướng dẫn cài đặt Thread Clone trên PythonAnywhere với Pusher

## 1. Chuẩn bị

- Tài khoản PythonAnywhere (có thể dùng tài khoản miễn phí)
- Tài khoản Pusher

## 2. Upload code lên PythonAnywhere

### Phương pháp 1: Sử dụng Git

```bash
# Trên PythonAnywhere Bash console
git clone https://github.com/your-github-username/thread-clone.git
cd thread-clone
pip install -r requirements.txt
```

### Phương pháp 2: Upload file thủ công

1. Nén dự án thành file ZIP
2. Upload qua PythonAnywhere Files tab
3. Giải nén trên PythonAnywhere

```bash
unzip thread-clone.zip
cd thread-clone
pip install -r requirements.txt
```

## 3. Cấu hình môi trường

1. Tạo file `.env` trong thư mục dự án với nội dung:

```
# Django settings
SECRET_KEY=your_generated_secret_key
DEBUG=False

# Database settings
DB_NAME=your_pythonanywhere_db_name
DB_USERNAME=your_pythonanywhere_db_username
DB_PASSWORD=your_pythonanywhere_db_password
DB_HOST=your_pythonanywhere_db_host
DB_PORT=3306

# Pusher settings
PUSHER_APP_ID=1985671
PUSHER_KEY=09581ace43aa27b85e17
PUSHER_SECRET=24b5d01464b02c6e48d4
PUSHER_CLUSTER=ap1

# Enable Pusher for PythonAnywhere
PYTHONANYWHERE_SITE=True
```

2. Thêm biến môi trường vào console hoặc WSGI file:

```python
import os
os.environ['PYTHONANYWHERE_SITE'] = 'True'
```

## 4. Cấu hình WSGI File

1. Vào tab **Web** trong PythonAnywhere
2. Tìm phần **Code** và click vào link WSGI configuration file
3. Thay thế nội dung với:

```python
import os
import sys

# Đường dẫn đến dự án - CHỈNH SỬA CHO PHÙ HỢP
path = '/home/yourusername/thread-clone'
if path not in sys.path:
    sys.path.append(path)

# Thiết lập biến môi trường cho Pusher
os.environ['PYTHONANYWHERE_SITE'] = 'True'

# Cấu hình Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# Khởi tạo WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 5. Cài đặt MySQL Database

1. Vào tab **Databases** trong PythonAnywhere
2. Tạo database mới
3. Cập nhật thông tin database trong file `.env`
4. Chạy migrations:

```bash
python manage.py migrate
```

## 6. Cấu hình Static Files

1. Trong tab **Web**, tìm phần **Static files**
2. Thêm:

   - URL: `/static/`
   - Directory: `/home/yourusername/thread-clone/staticfiles`
   - URL: `/media/`
   - Directory: `/home/yourusername/thread-clone/media`

3. Thu thập static files:

```bash
python manage.py collectstatic
```

## 7. Cấu hình CORS và CSRF

Trong file `settings.py` (đã được cập nhật), thêm domain PythonAnywhere của bạn vào:

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
    # Các origins khác...
]

CSRF_TRUSTED_ORIGINS = [
    "https://yourusername.pythonanywhere.com",
    # Các origins khác...
]
```

## 8. Kiểm tra hoạt động của Pusher

1. Vào [Pusher Dashboard](https://dashboard.pusher.com/)
2. Chọn ứng dụng của bạn
3. Chuyển đến tab Debug Console
4. Mở trang website của bạn trên PythonAnywhere
5. Thực hiện các hành động (like, comment) và kiểm tra xem các sự kiện có hiển thị trong Debug Console không

## 9. Khởi động lại webapp

1. Vào tab **Web**
2. Click nút **Reload** để khởi động lại ứng dụng

## Khắc phục sự cố

1. **Kiểm tra logs**: Vào tab Web > Logs để xem lỗi
2. **Vấn đề CORS**: Kiểm tra cấu hình CORS_ALLOWED_ORIGINS và CSRF_TRUSTED_ORIGINS
3. **Pusher không kết nối**:
   - Kiểm tra Debug Console của Pusher
   - Đảm bảo biến `PYTHONANYWHERE_SITE=True` đã được thiết lập
   - Kiểm tra thông tin Pusher trong `settings.py`
