# Hướng dẫn test WebSocket với Postman

## Chuẩn bị

1. Cài đặt [Postman](https://www.postman.com/downloads/)
2. Đảm bảo Django server (Daphne) đang chạy với lệnh: `python run_daphne.py`

## Tạo WebSocket Request trong Postman

### 1. Tạo Workspace mới (nếu cần)

1. Click vào "Workspaces" ở góc trên bên trái
2. Chọn "Create Workspace"
3. Đặt tên cho workspace (ví dụ: "Thread Clone WebSocket Test")
4. Click "Create"

### 2. Tạo WebSocket Request

1. Click vào "+" để tạo tab mới
2. Chọn "WebSocket Request" từ dropdown (hoặc click vào "New" > "WebSocket Request")
3. Nhập URL WebSocket:
   - Cho Thread: `ws://127.0.0.1:8000/ws/thread/{thread_id}/` (thay `{thread_id}` bằng ID thực)
   - Cho User: `ws://127.0.0.1:8000/ws/user/{user_id}/` (thay `{user_id}` bằng ID thực)

### 3. Thiết lập Authentication (nếu cần)

Nếu bạn cần xác thực, hãy thêm cookies:

1. Chọn tab "Headers" trong request
2. Thêm header: `Cookie` với giá trị: `sessionid=<your_session_id>` (lấy từ trình duyệt)

### 4. Kết nối đến WebSocket

1. Click nút "Connect" để kết nối đến WebSocket
2. Phần "Messages" sẽ hiển thị trạng thái kết nối

## Test các tính năng WebSocket

### 1. Test WebSocket Thread

#### Kết nối

1. Tạo WebSocket Request với URL: `ws://127.0.0.1:8000/ws/thread/1/` (hoặc ID thread khác)
2. Click "Connect"
3. Xác nhận kết nối thành công ("Connection established")

#### Tạo sự kiện từ API endpoints

Trong khi kết nối WebSocket mở, thực hiện các hành động sau bằng API requests thông thường:

**Like Thread:**

1. Tạo một "HTTP Request" mới
2. Chọn phương thức "POST"
3. URL: `http://127.0.0.1:8000/api/threads/1/like/` (thay `1` bằng ID thread)
4. Headers:
   - `Content-Type: application/json`
   - `X-CSRFToken: <your_csrf_token>`
   - `Cookie: sessionid=<your_session_id>`
5. Click "Send"
6. Xem phản hồi từ WebSocket (sẽ hiển thị trong tab WebSocket với dữ liệu cập nhật về số lượng like)

**Thêm Comment:**

1. Tạo một "HTTP Request" mới
2. Chọn phương thức "POST"
3. URL: `http://127.0.0.1:8000/api/threads/1/comments/`
4. Headers:
   - `Content-Type: application/json`
   - `X-CSRFToken: <your_csrf_token>`
   - `Cookie: sessionid=<your_session_id>`
5. Body (raw JSON):
   ```json
   {
     "content": "Đây là comment test từ Postman"
   }
   ```
6. Click "Send"
7. Xem phản hồi từ WebSocket (sẽ hiển thị thông tin về comment mới)

### 2. Test WebSocket User Notifications

#### Kết nối

1. Tạo WebSocket Request với URL: `ws://127.0.0.1:8000/ws/user/1/` (thay `1` bằng ID user của bạn)
2. Click "Connect"
3. Xác nhận kết nối thành công

#### Kích hoạt thông báo

Thực hiện các hành động để kích hoạt thông báo, ví dụ:

- Like một thread của người khác
- Comment trên thread của người khác
- Follow người khác

**Ví dụ - Like Thread để tạo thông báo:**

1. Tạo một "HTTP Request" mới
2. Chọn phương thức "POST"
3. URL: `http://127.0.0.1:8000/api/threads/2/like/` (thay `2` bằng ID thread của người dùng khác)
4. Headers:
   - `Content-Type: application/json`
   - `X-CSRFToken: <your_csrf_token>`
   - `Cookie: sessionid=<your_session_id>`
5. Click "Send"
6. Xem thông báo mới trong tab WebSocket của user

## Lấy CSRF Token và Session ID

### Lấy CSRF Token:

1. Tạo HTTP Request mới
2. Phương thức: "GET"
3. URL: `http://127.0.0.1:8000/api/csrf/`
4. Click "Send"
5. Sao chép token từ phản hồi

### Lấy Session ID:

1. Đăng nhập vào webapp trong trình duyệt
2. Mở Developer Tools (F12)
3. Chọn tab "Application" > "Cookies"
4. Sao chép giá trị của cookie `sessionid`

## Tips

1. **Theo dõi dữ liệu:** Khi kết nối WebSocket, tất cả dữ liệu gửi/nhận sẽ hiển thị trong tab "Messages"
2. **Lưu requests:** Lưu các WebSocket requests để tái sử dụng sau này
3. **Collection:** Tạo collection cho các request liên quan để dễ quản lý
4. **Môi trường (Environment):** Sử dụng môi trường Postman để lưu trữ các biến như token, session ID

## Troubleshooting

- **Lỗi kết nối 403:** Kiểm tra session ID và đảm bảo đã đăng nhập
- **Không nhận được thông báo:** Kiểm tra xem bạn đã kết nối đúng endpoint và user ID chưa
- **Lỗi CORS:** Đây là lỗi phổ biến khi test WebSocket, hãy đảm bảo cài đặt CORS trong Django đã được cấu hình đúng
