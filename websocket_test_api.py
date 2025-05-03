import websocket
import json
import requests
import threading
import time

# Cấu hình
BASE_URL = "http://127.0.0.1:8000"
WS_BASE_URL = "ws://127.0.0.1:8000"
THREAD_ID = 1  # Thay đổi ID thread phù hợp
USER_ID = 1    # Thay đổi ID user phù hợp
SESSION_ID = ""  # Nhập session ID của bạn vào đây

# Đường dẫn WebSocket
THREAD_WS_URL = f"{WS_BASE_URL}/ws/thread/{THREAD_ID}/"
USER_WS_URL = f"{WS_BASE_URL}/ws/user/{USER_ID}/"

# Đường dẫn API
CSRF_URL = f"{BASE_URL}/api/csrf/"
THREAD_LIKE_URL = f"{BASE_URL}/api/threads/{THREAD_ID}/like/"
THREAD_COMMENT_URL = f"{BASE_URL}/api/threads/{THREAD_ID}/comments/"

# Hàm lấy CSRF token
def get_csrf_token():
    response = requests.get(CSRF_URL, cookies={"sessionid": SESSION_ID})
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("csrfToken")
    else:
        print(f"Lỗi khi lấy CSRF token: {response.status_code}")
        return None

# Callback cho WebSocket
def on_message(ws, message):
    print("\n[Tin nhắn WebSocket]")
    try:
        data = json.loads(message)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(message)

def on_error(ws, error):
    print(f"\n[Lỗi WebSocket] {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"\n[WebSocket đã đóng] Mã: {close_status_code}, Tin nhắn: {close_msg}")

def on_open(ws):
    print("\n[WebSocket đã kết nối]")

# Hàm kết nối WebSocket
def connect_websocket(url, name="WebSocket"):
    ws = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=["Cookie: sessionid=" + SESSION_ID] if SESSION_ID else None
    )
    
    print(f"\n[Đang kết nối {name}...]")
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()
    return ws

# Hàm thực hiện các hành động API
def like_thread():
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("Không thể lấy CSRF token, không thể tiếp tục.")
        return
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
    }
    cookies = {"sessionid": SESSION_ID} if SESSION_ID else None
    
    print(f"\n[Gửi yêu cầu like thread {THREAD_ID}...]")
    response = requests.post(
        THREAD_LIKE_URL, 
        headers=headers, 
        cookies=cookies
    )
    
    if response.status_code == 200:
        print("[Like thành công] Phản hồi:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"[Lỗi like] Mã: {response.status_code}")
        try:
            print(response.json())
        except:
            print(response.text)

def add_comment(content="Test comment từ Python script"):
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("Không thể lấy CSRF token, không thể tiếp tục.")
        return
    
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
    }
    cookies = {"sessionid": SESSION_ID} if SESSION_ID else None
    
    data = {"content": content}
    
    print(f"\n[Gửi comment đến thread {THREAD_ID}...]")
    response = requests.post(
        THREAD_COMMENT_URL, 
        headers=headers, 
        cookies=cookies,
        json=data
    )
    
    if response.status_code in [200, 201]:
        print("[Comment thành công] Phản hồi:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"[Lỗi comment] Mã: {response.status_code}")
        try:
            print(response.json())
        except:
            print(response.text)

# Hàm menu cho người dùng
def show_menu():
    while True:
        print("\n--- MENU TEST WEBSOCKET ---")
        print("1. Kết nối Thread WebSocket")
        print("2. Kết nối User WebSocket")
        print("3. Like thread")
        print("4. Thêm comment")
        print("5. Đóng tất cả kết nối")
        print("0. Thoát")
        
        choice = input("\nNhập lựa chọn: ")
        
        if choice == "1":
            thread_ws = connect_websocket(THREAD_WS_URL, "Thread WebSocket")
        elif choice == "2":
            user_ws = connect_websocket(USER_WS_URL, "User WebSocket")
        elif choice == "3":
            like_thread()
        elif choice == "4":
            content = input("Nhập nội dung comment: ")
            add_comment(content if content else "Test comment từ Python script")
        elif choice == "5":
            print("Đóng tất cả kết nối WebSocket...")
            # Nếu đã tạo các kết nối, đóng chúng ở đây
        elif choice == "0":
            print("Thoát chương trình...")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

if __name__ == "__main__":
    print("=== WebSocket Test Tool ===")
    
    # Kiểm tra session ID
    if not SESSION_ID:
        print("\nCHÚ Ý: Session ID chưa được thiết lập.")
        print("Một số chức năng có thể không hoạt động nếu cần xác thực.")
        
        use_session = input("Bạn có muốn nhập Session ID không? (y/n): ")
        if use_session.lower() == "y":
            SESSION_ID = input("Nhập Session ID: ")
    
    show_menu() 