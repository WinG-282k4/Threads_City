# Thread Clone API

## API Documentation

### 1. Authentication APIs (`/api/auth/users/`)

#### User Registration

- **Endpoint**: `POST /api/auth/users/`
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

#### User Login

- **Endpoint**: `POST /api/auth/users/login/`
- **Body**:
  ```json
  {
    "username": "username",
    "password": "password"
  }
  ```

#### Get Current User

- **Endpoint**: `GET /api/auth/users/me/`
- **Authentication**: Required

#### Change Password

- **Endpoint**: `POST /api/auth/users/change_password/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "old_password": "oldpassword",
    "new_password": "newpassword"
  }
  ```

### 2. Thread APIs (`/api/threads/`)

#### Get All Threads

- **Endpoint**: `GET /api/threads/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)

#### Get Thread Feed

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
    "content": "Thread content here"
  }
  ```

#### Like Thread

- **Endpoint**: `POST /api/threads/{thread_id}/like/`
- **Authentication**: Required

#### Repost Thread

- **Endpoint**: `POST /api/threads/{thread_id}/repost/`
- **Authentication**: Required

### 3. Comment APIs (`/api/threads/{thread_id}/comments/`)

#### Get Thread Comments

- **Endpoint**: `GET /api/threads/{thread_id}/comments/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)

#### Create Comment

- **Endpoint**: `POST /api/threads/{thread_id}/comments/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "content": "Comment content here"
  }
  ```

#### Like Comment

- **Endpoint**: `POST /api/threads/{thread_id}/comments/{comment_id}/like/`
- **Authentication**: Required

#### Repost Comment

- **Endpoint**: `POST /api/threads/{thread_id}/comments/{comment_id}/repost/`
- **Authentication**: Required

### 4. Follow APIs (`/api/follows/`)

#### Get Following List

- **Endpoint**: `GET /api/follows/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)

#### Follow User

- **Endpoint**: `POST /api/follows/`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "followed": user_id
  }
  ```

### 5. Notification APIs (`/api/notifications/`)

#### Get Notifications

- **Endpoint**: `GET /api/notifications/`
- **Authentication**: Required
- **Query Params**: `?page=1` (pagination)

#### Get Unread Notification Count

- **Endpoint**: `GET /api/notifications/unread_count/`
- **Authentication**: Required

#### Mark Notification as Read

- **Endpoint**: `POST /api/notifications/{notification_id}/mark_read/`
- **Authentication**: Required

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
