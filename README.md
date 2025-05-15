# Thread Clone API

## API Documentation

### Response Format

Most API responses follow this format:

#### Success Response for Create/Update Operations

```json
{
  "status": "success",
  "data": {
    // Response data here
  }
}
```

#### Error Response for Create/Update Operations

```json
{
  "status": "error",
  "errors": {
    // Error messages here
  }
}
```

#### List/Get Operations Response

List and get operations return data directly without status wrapper:

```json
{
  "count": 10,
  "next": "http://api.example.org/endpoint/?page=2",
  "previous": null,
  "results": [
    // Array of items
  ]
}
```

### CSRF Token

#### Get CSRF Token

- **Endpoint**: `GET /api/csrf/`
- **Authentication**: Not Required
- **Description**: Get CSRF token for making POST/PUT/DELETE requests
- **Response**:
  ```json
  {
    "status": "success",
    "data": {
      "csrfToken": "your-csrf-token"
    }
  }
  ```
- **Usage**:
  1. Call this endpoint first
  2. Get token from both response and cookie
  3. Include token in subsequent requests:
     ```
     X-CSRFToken: your-csrf-token
     ```
  4. In development mode, CSRF tokens are served over HTTP (not requiring HTTPS)
     and use Lax same-site policy.

### Content Moderation

The API includes automatic content moderation for threads and comments. When creating a thread or comment, the content is checked against a toxicity detection API. If the content is flagged as toxic:

1. The creation will be rejected with an appropriate error message
2. A notification will be sent to the user informing them that their content violated community standards

#### Thread Creation Error (Toxic Content)

```json
{
  "status": "error",
  "errors": {
    "content": "Bài viết của bạn vi phạm tiêu chuẩn cộng đồng"
  }
}
```

#### Comment Creation Error (Toxic Content)

```json
{
  "status": "error",
  "errors": {
    "content": "Bình luận của bạn vi phạm tiêu chuẩn cộng đồng"
  }
}
```

#### Toxic Content Notifications

When toxic content is detected, a notification is sent to the user who attempted to post the content. The user will see a notification with the message "Bài viết của bạn vi phạm tiêu chuẩn cộng đồng và đã bị từ chối" (for threads) or "Bình luận của bạn vi phạm tiêu chuẩn cộng đồng và đã bị từ chối" (for comments).

### 1. Authentication APIs (`/api/auth/users/`)

#### User Registration

- **Endpoint**: `POST /api/auth/users/`
- **Authentication**: Not Required
- **Body**:
  ```json
  {
    "username": "newuser",
    "password": "password123",
    "password2": "password123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

````

- **Success Response**:
  ```json
  {
    "status": "success",
    "data": {
      "id": 1,
      "username": "newuser",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "avatar": "url_to_avatar_image"
    }
  }
````

#### User Login

- **Endpoint**: `POST /api/auth/users/login/`
- **Authentication**: Not Required
- **Body**:
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```

````
- **Success Response**:
  ```json
  {
    "status": "success",
    "data": {
      "id": 1,
      "username": "username",
      "email": "email@example.com",
      "first_name": "First",
      "last_name": "Last",
      "date_joined": "2024-03-21T10:00:00Z",
      "avatar": "url_to_avatar_image"
    }
  }
````

#### Get Current User

- **Endpoint**: `GET /api/auth/users/me/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "status": "success",
    "data": {
      "id": 25,
      "username": "NPThanh12345",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_joined": "2025-05-12T18:01:31.512704+06:30",
      "avatar": "https://img.freepik.com/premium-vector/user-profile-person-avatar-identity-login-icon-vector_1277826-995.jpg?w=360"
    }
  }
  ```

````

#### Update Current User

- **Endpoint**: `PUT/PATCH /api/auth/users/update_me/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "email": "new.email@example.com",
    "first_name": "New First Name",
    "last_name": "New Last Name",
    "avatar": "new_avatar_link",
    "bio": "New bio text"
  }
````

- **Success Response**:
  ```json
  {
    "status": "success",
    "data": {
      "id": 1,
      "username": "username",
      "email": "new.email@example.com",
      "first_name": "New First Name",
      "last_name": "New Last Name",
      "date_joined": "2024-03-21T10:00:00Z",
      "avatar": "new_avatar_link"
    }
  }
  ```

````

#### Change Password

- **Endpoint**: `POST /api/auth/users/change_password/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "old_password": "oldpassword",
    "new_password": "newpassword",
    "new_password2": "newpassword"
  }
````

- **Success Response**:
  ```json
  {
    "status": "success",
    "data": {
      "message": "Password changed successfully"
    }
  }
  ```

````

#### User Logout

- **Endpoint**: `POST /api/auth/users/logout/`
- **Authentication**: Required
- **Description**: Logs out the current user by removing their session and all related cookies
- **Success Response**:
  ```json
    {
      "status": "success",
      "data": {
        "message": "Logged out successfully"
      }
    }
  ```
- **Effect**: This API không chỉ xóa session của người dùng trên server mà còn xóa các cookie liên quan đến phiên đăng nhập (`sessionid` và `csrftoken`) trên trình duyệt của người dùng

#### Search Users

- **Endpoint**: `GET /api/users/?search=query`
- **Authentication**: Required
- **Query Params**:
  - `search`: Search query (username, first name, or last name)
  - `page`: Page number for pagination
- **Response**:
  ```json
  {
    "count": 5,
    "next": "http://api.example.org/users/?search=query&page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "username": "username",
        "first_name": "First",
        "last_name": "Last",
        "email": "email@example.com",
        "avatar": "url_to_avatar_image"
      }
    ]
  }
````

#### Get User Details

- **Endpoint**: `GET /api/users/{user_id}/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "id": 1,
    "username": "username",
    "first_name": "First",
    "last_name": "Last",
    "email": "email@example.com",
    "avatar": "url_to_avatar_image",
    "threads": [
      {
        "id": 1,
        "content": "Thread content",
        "created_at": "2024-03-21T10:00:00Z",
        "likes_count": 5,
        "reposts_count": 3,
        "comment_count": 10,
        "images": [
          {
            "id": 1,
            "image": "url_to_thread_image"
          }
        ]
      }
    ],
    "reposted_threads": [
      {
        "id": 2,
        "content": "Reposted thread content",
        "created_at": "2024-03-22T10:00:00Z",
        "likes_count": 8,
        "reposts_count": 4,
        "comment_count": 12,
        "images": [
          {
            "id": 2,
            "image": "url_to_reposted_thread_image"
          }
        ]
      }
    ],
    "is_followed": true,
    "followers_count": 120
  }
  ```

### 2. Thread APIs (`/api/threads/`)

#### Get All Threads

- **Endpoint**: `GET /api/threads/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)
- **Response**:
  ```json
  {
    "count": 10,
    "next": "http://api.example.org/threads/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "content": "Thread content",
        "user": {
          "id": 1,
          "username": "username",
          "first_name": "First",
          "last_name": "Last",
          "email": "email@example.com",
          "avatar": "url_to_avatar_image"
        },
        "images": [
          {
            "id": 1,
            "image": "url_to_thread_image"
          }
        ],
        "created_at": "2024-03-21T10:00:00Z",
        "comments": [],
        "likes_count": 5,
        "is_liked": false,
        "reposts_count": 3,
        "is_reposted": false,
        "comment_count": 10
      }
    ]
  }
  ```

#### Get Thread Feed: giống với `GET /api/threads/` nhưng chỉ có thể đọc

- **Endpoint**: `GET /api/threads/feed/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)

#### Get Following Feed

- **Endpoint**: `GET /api/threads/following_feed/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)

#### Get My Threads

- **Endpoint**: `GET /api/threads/my_threads/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)
- **Description**: Lấy tất cả thread do user hiện tại tạo
- **Response**: Giống format của Get All Threads

#### Get My Commented Threads

- **Endpoint**: `GET /api/threads/my_commented_threads/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)
- **Description**: Lấy tất cả thread mà user hiện tại đã comment (không bao gồm thread do user tạo)
- **Response**: Giống format của Get All Threads

#### Get My Reposted Threads

- **Endpoint**: `GET /api/threads/my_reposted_threads/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)
- **Description**: Lấy tất cả thread mà user hiện tại đã repost
- **Response**: Giống format của Get All Threads

#### Get User Threads

- **Endpoint**: `GET /api/threads/user_threads/`
- **Authentication**: Required
- **Query Params**:
  - `user_id`: ID của user cần lấy thread
  - `page`: Số trang (pagination)
- **Description**: Lấy tất cả thread của một user (bao gồm cả thread do user tạo và thread user đã repost)
- **Response**: Giống format của Get All Threads
- **Error Responses**:
  - 400 Bad Request: Khi thiếu tham số `user_id`
  - 404 Not Found: Khi không tìm thấy user với ID đã cho

#### Create Thread

- **Endpoint**: `POST /api/threads/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "content": "Thread content",
    "images": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ]
  }
  ```

````

- **Success Response**:
  ```json
  {
    "id": 1,
    "content": "Thread content",
    "user": {
      "id": 1,
      "username": "username",
      "first_name": "First",
      "last_name": "Last",
      "avatar": "url_to_avatar_image"
    },
    "images": [
      {
        "id": 1,
        "image": "https://example.com/image1.jpg"
      }
    ],
    "created_at": "2024-03-21T10:00:00Z",
    "likes_count": 0,
    "is_liked": false,
    "reposts_count": 0,
    "is_reposted": false,
    "comment_count": 0
  }
  ```

````

- **Error Response (Toxic Content)**:
  ```json
  {
    "status": "error",
    "errors": {
      "content": "Bài viết của bạn vi phạm tiêu chuẩn cộng đồng"
    }
  }
  ```

````

#### Like/Unlike Thread

- **Endpoint**: `POST /api/threads/{thread_id}/like/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "likes_count": 6,
    "is_liked": true
  }
  ```

````

#### Repost/Unrepost Thread

- **Endpoint**: `POST /api/threads/{thread_id}/repost/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "reposts_count": 4,
    "is_reposted": true
  }
  ```

````

#### Delete Thread

- **Endpoint**: `DELETE /api/threads/{thread_id}/`
- **Authentication**: Required
- **Description**: Delete a thread. You can only delete your own threads.
- **Success Response**:
  ```json
  {
    "status": "success",
    "data": {
      "message": "Thread deleted successfully"
    }
  }
  ```
- **Error Response (Not Owner)**:
  ```json
  {
    "status": "error",
    "errors": {
      "detail": "You can only delete your own threads"
    }
  }
  ```

### 3. Comment APIs (`/api/threads/{thread_id}/comments/`)

#### Get Comments for a Thread

- **Endpoint**: `GET /api/threads/{thread_id}/comments/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "count": 10,
    "next": "http://api.example.org/threads/1/comments/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "content": "Comment content",
        "user": {
          "id": 1,
          "username": "username",
          "first_name": "First",
          "last_name": "Last",
          "email": "email@example.com",
          "avatar": "url_to_avatar_image"
        },
        "created_at": "2024-03-21T10:00:00Z",
        "likes_count": 5,
        "is_liked": false,
        "replies_count": 3
      }
    ]
  }
  ```

````

#### Get Replies for a Comment

- **Endpoint**: `GET /api/threads/{thread_id}/comments/{comment_id}/replies/`
- **Authentication**: Required
- **Response**:

```json
[
  {
    "id": 2,
    "content": "Reply content",
    "user": {
      "id": 1,
      "username": "username",
      "first_name": "First",
      "last_name": "Last",
      "email": "email@example.com",
      "avatar": "url_to_avatar_image"
    },
    "created_at": "2024-03-21T10:00:00Z",
    "likes_count": 2,
    "is_liked": false,
    "replies_count": 0
  }
]
```

#### Create Comment

- **Endpoint**: `POST /api/threads/{thread_id}/comments/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "content": "Your comment content",
    "parent_comment_id": null
  }
  ```

````

- **Success Response**:
  ```json
  {
    "id": 21,
    "content": "test lại respone thread mới",
    "user": {
      "id": 21,
      "username": "newuserthanh7",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_joined": "2025-03-21T10:12:52.191155+06:30",
      "avatar": null
    },
    "created_at": "2025-03-21T10:29:21.587547+06:30",
    "likes_count": 0,
    "is_liked": false,
    "replies_count": 0
  }
  ```

````

#### Like/Unlike Comment

- **Endpoint**: `POST /api/threads/{thread_id}/comments/{comment_id}/like/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "likes_count": 6,
    "is_liked": true
  }
  ```

````

#### Repost/Unrepost Comment

- **Endpoint**: `POST /api/threads/{thread_id}/comments/{comment_id}/repost/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "reposts_count": 4,
    "is_reposted": true
  }
  ```

````

### 4. Follow APIs (`/api/follows/`)

#### Get Following List

- **Endpoint**: `GET /api/follows/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)
- **Response**:
  ```json
  {
    "count": 10,
    "next": "http://api.example.org/follows/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "follower": {
          "id": 1,
          "username": "username",
          "first_name": "First",
          "last_name": "Last",
          "email": "email@example.com",
          "avatar": "url_to_avatar_image"
        },
        "followed": {
          "id": 2,
          "username": "username2",
          "first_name": "First2",
          "last_name": "Last2",
          "email": "email2@example.com",
          "avatar": "url_to_avatar_image2"
        },
        "created_at": "2024-03-21T10:00:00Z"
      }
    ]
  }
  ```

````

#### Follow/Unfollow User

- **Endpoint**: `POST /api/follows/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "followed_id": 2
  }
  ```

````

- **Success Response**:
  ```json
  {
    "id": 7,
    "follower": {
      "id": 21,
      "username": "newuserthanh7",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_joined": "2025-03-21T10:12:52.191155+06:30",
      "avatar": null
    },
    "followed": {
      "id": 2,
      "username": "testuser2",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_joined": "2025-03-19T22:24:54.388729+06:30",
      "avatar": "Test avatar"
    },
    "created_at": "2025-03-21T10:30:18.530447+06:30",
    "status": "Followed successfully"
  }
  ```

````

#### Get Followers Count

- **Endpoint**: `GET /api/follows/followers_count/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "count": 123
  }
  ```

````

### 5. Notification APIs (`/api/notifications/`)

#### Get Notifications

- **Endpoint**: `GET /api/notifications/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)
- **Response**:
  ```json
  {
    "count": 10,
    "next": "http://api.example.org/notifications/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "user": {
          "id": 1,
          "username": "username",
          "first_name": "First",
          "last_name": "Last",
          "email": "email@example.com",
          "avatar": "url_to_avatar_image"
        },
        "actioner": {
          "id": 2,
          "username": "username2",
          "first_name": "First2",
          "last_name": "Last2",
          "email": "email2@example.com",
          "avatar": "url_to_avatar_image2"
        },
        "content": "Notification content",
        "created_at": "2024-03-21T10:00:00Z",
        "is_read": false
      }
    ]
  }
  ```

````

#### Get Unread Notification Count

- **Endpoint**: `GET /api/notifications/unread_count/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "count": 5
  }
  ```

````

#### Mark Notification as Read

- **Endpoint**: `POST /api/notifications/{notification_id}/mark_read/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "id": 1,
    "is_read": true
  }
  ```

````

#### Mark All Notifications as Read

- **Endpoint**: `POST /api/notifications/mark_all_read/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "message": "All notifications marked as read"
  }
  ```

````

#### Get Unread Notifications

- **Endpoint**: `GET /api/notifications/?is_read=false`
- **Authentication**: Required
- **Query Params**:
  - `is_read`: false
  - `page`: Page number for pagination
- **Response**: Same as Get Notifications endpoint

### WebSocket/Real-time Updates

The application supports real-time updates using WebSockets. The implementation automatically switches between:

- **Django Channels**: Used in development/local environment
- **Pusher**: Used when deployed on PythonAnywhere (which doesn't support WebSockets on free tiers)

#### Connection Details

##### Django Channels (Local Development)

- **Thread Channel**: `ws://localhost:8000/ws/thread/{thread_id}/`
- **User Notification Channel**: `ws://localhost:8000/ws/user/{user_id}/`

##### Pusher (Production/PythonAnywhere)

- **Thread Channel**: `thread_{thread_id}`
- **User Notification Channel**: `user_{user_id}`
- **Events**: Same event names as Django Channels

#### Authentication

- **Django Channels**: Authentication via session cookie (`sessionid`)
- **Pusher**: Client-side subscription with public key

#### Events & Payloads

##### Thread Updates

1. **Like Update**

   - **Event**: `like_update`
   - **Data**:
     ```json
     {
       "type": "like_update",
       "thread_id": 1,
       "likes_count": 10,
       "action": "like" or "unlike"
     }
     ```

2. **Comment Like Update**

   - **Event**: `like_update`
   - **Data**:
     ```json
     {
       "type": "comment_like_update",
       "thread_id": 1,
       "comment_id": 2,
       "likes_count": 5,
       "action": "like" or "unlike"
     }
     ```

3. **New Comment**

   - **Event**: `comment_update`
   - **Data**:
     ```json
     {
       "type": "new_comment",
       "thread_id": 1,
       "comment_id": 3,
       "content": "Comment content",
       "comment_count": 15,
       "is_reply": false,
       "parent_comment_id": null,
       "user_info": {
         "id": 1,
         "username": "username",
         "avatar": "url_to_avatar_image"
       }
     }
     ```

4. **Comment Deleted**

   - **Event**: `comment_update`
   - **Data**:
     ```json
     {
       "type": "comment_deleted",
       "thread_id": 1,
       "comment_count": 14
     }
     ```

5. **Reply Deleted**
   - **Event**: `comment_update`
   - **Data**:
     ```json
     {
       "type": "reply_deleted",
       "thread_id": 1,
       "parent_comment_id": 2,
       "replies_count": 3
     }
     ```

##### User Notifications

1. **New Notification**
   - **Event**: `notification_update`
   - **Data**:
     ```json
     {
       "type": "new_notification",
       "notification_id": 1,
       "notification_type": "like_thread" | "like_comment" | "comment_reply" |
                           "thread_comment" | "follow" | "repost_thread" |
                           "repost_comment" | "toxic_content",
       "content": "Notification content"
     }
     ```

#### Frontend Implementation

##### Pusher (JavaScript Example)

```javascript
// Initialize Pusher
const pusher = new Pusher("your_pusher_key", {
  cluster: "your_pusher_cluster",
  forceTLS: true,
});

// Subscribe to a thread channel
const threadChannel = pusher.subscribe(`thread_${threadId}`);

// Listen for like updates
threadChannel.bind("like_update", function (data) {
  // Update UI with new like count
  console.log(`Thread ${data.thread_id} now has ${data.likes_count} likes`);
});

// Subscribe to user notifications
const userChannel = pusher.subscribe(`user_${userId}`);

// Listen for new notifications
userChannel.bind("notification_update", function (data) {
  // Update UI with new notification
  console.log(`New notification: ${data.content}`);
});
```

##### Django Channels (JavaScript WebSocket Example)

```javascript
// Connect to thread WebSocket
const threadSocket = new WebSocket(
  `ws://localhost:8000/ws/thread/${threadId}/`
);

// Handle messages
threadSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.type === "like_update") {
    // Update UI with new like count
    console.log(`Thread ${data.thread_id} now has ${data.likes_count} likes`);
  } else if (data.type === "comment_update") {
    // Handle comment updates
    console.log(`New comment on thread ${data.thread_id}`);
  }
};

// Connect to user notification WebSocket
const userSocket = new WebSocket(`ws://localhost:8000/ws/user/${userId}/`);

// Handle notifications
userSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  if (data.type === "notification_update") {
    // Update UI with new notification
    console.log(`New notification: ${data.content}`);
  }
};
```

### Authentication & Headers

All APIs (except registration and login) require authentication. Required headers:

```
Content-Type: application/json
Accept: application/json
Authorization: Bearer <access_token>  # For JWT authentication
```

Authentication methods supported:

- JWT Authentication (Bearer token)
- Session Authentication
- Basic Authentication

#### JWT Authentication

- Access Token: Valid for 60 minutes
- Refresh Token: Valid for 1 day
- Login response includes both tokens:
  ```json
  {
    "user": {
      "id": 1,
      "username": "username",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
  }
  ```

````

### Pagination

- Default: 10 items per page
- Query parameter: `?page=1`

### Error Responses

```json
{
  "detail": "Error message here"
}
```

Status codes:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Development Setup

1. Clone the repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Create config.py with required settings
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`
````
