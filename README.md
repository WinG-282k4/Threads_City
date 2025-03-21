# Thread Clone API

## API Documentation

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
- **Response**:
  ```json
  {
    "id": 1,
    "username": "newuser",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "avatar": "url_to_avatar_image"
  }
  ```

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
- **Response**: JWT Token

#### Get Current User

- **Endpoint**: `GET /api/auth/users/me/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "id": 1,
    "username": "username",
    "email": "email@example.com",
    "first_name": "First",
    "last_name": "Last",
    "date_joined": "2024-03-21T10:00:00Z",
    "avatar": "url_to_avatar_image"
  }
  ```

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
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "username": "username",
    "email": "new.email@example.com",
    "first_name": "New First Name",
    "last_name": "New Last Name",
    "date_joined": "2024-03-21T10:00:00Z",
    "avatar": "new_avatar_link"
  }
  ```

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
  ```
- **Response**:
  ```json
  {
    "status": "password set"
  }
  ```
- **Error Response**:
  ```json
  {
    "new_password": ["Password fields didn't match."]
  }
  ```
  OR
  ```json
  {
    "old_password": ["Wrong password."]
  }
  ```

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
  ```

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
    "avatar": "url_to_avatar_image"
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
        "comments": [...],
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

#### Create Thread

- **Endpoint**: `POST /api/threads/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "content": "Thread content here",
    "images": ["image1.jpg", "image2.jpg"]
  }
  ```
- **Response**: Created thread object with same structure as GET response

#### Like Thread

- **Endpoint**: `POST /api/threads/{thread_id}/like/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "status": "success"
  }
  ```

#### Repost Thread

- **Endpoint**: `POST /api/threads/{thread_id}/repost/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "status": "success"
  }
  ```

### 3. Comment APIs (`/api/threads/{thread_id}/comments/`)

#### Get Comments for a Thread

- **Endpoint**: `GET /api/threads/{thread_id}/comments/`
- **Authentication**: Required
- **Response**:

```json
[
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
```

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

#### Create a Comment

- **Endpoint**: `POST /api/threads/{thread_id}/comments/`
- **Authentication**: Required
- **Body**:

```json
{
  "content": "Your comment content",
  "parent_comment_id": null // Optional: ID of parent comment if this is a reply
}
```

- **Response**: Created comment object with same structure as GET response

#### Like/Unlike a Comment

```http
POST /api/threads/{thread_id}/comments/{comment_id}/like/
```

Response:

```json
{
  "status": "success"
}
```

#### Repost/Unrepost a Comment

```http
POST /api/threads/{thread_id}/comments/{comment_id}/repost/
```

Response:

```json
{
  "status": "success"
}
```

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
        "created_at": "2024-03-21T10:00:00Z",
        "status": "Followed successfully"
      }
    ]
  }
  ```

#### Follow/Unfollow User

- **Endpoint**: `POST /api/follows/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "followed_id": user_id
  }
  ```
- **Response**: Follow object with same structure as GET response

#### Get Followers Count

- **Endpoint**: `GET /api/follows/followers_count/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "count": 123
  }
  ```

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

#### Get Unread Notification Count

- **Endpoint**: `GET /api/notifications/unread_count/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "count": 5
  }
  ```

#### Mark Notification as Read

- **Endpoint**: `POST /api/notifications/{notification_id}/mark_read/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "status": "success",
    "id": 1
  }
  ```

#### Mark All Notifications as Read

- **Endpoint**: `POST /api/notifications/mark_all_read/`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "status": "success",
    "message": "All notifications marked as read"
  }
  ```

#### Get Unread Notifications

- **Endpoint**: `GET /api/notifications/?is_read=false`
- **Authentication**: Required
- **Query Params**:
  - `is_read`: false
  - `page`: Page number for pagination
- **Response**: Same as Get Notifications endpoint

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
