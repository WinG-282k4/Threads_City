# Hướng dẫn triển khai dự án lên Render

## Bước 1: Tạo tài khoản Render

1. Truy cập [Render.com](https://render.com)
2. Đăng ký tài khoản mới hoặc đăng nhập nếu đã có tài khoản

## Bước 2: Kết nối với GitHub

1. Đăng nhập vào Render
2. Vào Dashboard và chọn "New +"
3. Chọn "Web Service"
4. Kết nối với GitHub repository của bạn

## Bước 3: Cấu hình Web Service

1. Đặt tên cho dịch vụ (ví dụ: thread-clone)
2. Chọn Region gần vị trí của bạn
3. Chọn Runtime: Python
4. Điền vào các thông tin sau:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && chmod +x run.sh run_gunicorn.sh`
   - Start Command: `./run.sh`

## Bước 4: Thiết lập biến môi trường

Thêm các biến môi trường sau đây:

```
DJANGO_SETTINGS_MODULE=core.settings
SECRET_KEY=<your_secret_key>
DEBUG=False
DB_NAME=<your_railway_db_name>
DB_USERNAME=<your_railway_db_username>
DB_PASSWORD=<your_railway_db_password>
DB_HOST=<your_railway_db_host>
DB_PORT=3306
```

Đảm bảo rằng tất cả thông tin kết nối database đều chính xác (lấy từ Railway).

## Bước 5: Cập nhật CORS và CSRF settings

Vào file `core/settings.py` và thêm domain của Render vào:

```python
CSRF_TRUSTED_ORIGINS = [
    # Các origins hiện tại
    'https://your-app-name.onrender.com',
]

CORS_ALLOWED_ORIGINS = [
    # Các origins hiện tại
    'https://your-app-name.onrender.com',
]
```

## Bước 6: Deploy

1. Nhấn "Create Web Service"
2. Render sẽ bắt đầu quá trình xây dựng và triển khai dự án của bạn
3. Đợi quá trình hoàn tất (có thể mất 5-10 phút)

## Bước 7: Kiểm tra

1. Mở URL được cung cấp bởi Render (https://your-app-name.onrender.com)
2. Kiểm tra xem ứng dụng đã hoạt động chưa

## Xử lý lỗi DJANGO_SETTINGS_MODULE

Nếu gặp lỗi liên quan đến biến môi trường DJANGO_SETTINGS_MODULE, hãy thử một trong các cách sau:

1. **Sử dụng file run.sh**:

   ```bash
   #!/bin/bash
   # Thiết lập biến môi trường Django
   export DJANGO_SETTINGS_MODULE=core.settings

   # Chạy daphne với cổng từ biến môi trường
   daphne -b 0.0.0.0 -p $PORT core.asgi:application
   ```

2. **Sử dụng Gunicorn thay vì Daphne** (nếu WebSockets không quan trọng):

   - Thay đổi Start Command thành: `./run_gunicorn.sh` hoặc `gunicorn --bind 0.0.0.0:$PORT core.wsgi:application`

3. **Kiểm tra logs** trong Render Dashboard để xem lỗi chi tiết

## Ghi chú

- Đảm bảo các thông tin kết nối database từ Railway đã được cập nhật chính xác
- Nếu bạn cần chạy migrations, có thể sử dụng "Shell" trong Render Dashboard và chạy lệnh `python manage.py migrate`
- Để xem logs chi tiết, vào phần "Logs" trong Render Dashboard
