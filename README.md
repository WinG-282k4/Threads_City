# Thread Clone API

## Authentication APIs

### User Authentication

```
POST   /api/auth/users/login/           # Login
POST   /api/auth/users/                 # Register
GET    /api/auth/users/me/              # Get current user
PUT    /api/auth/users/me/              # Update current user
POST   /api/auth/users/change_password/ # Change password
```

### User Management

```
GET    /api/auth/users/                 # List all users
GET    /api/auth/users/{id}/            # Get user detail
PUT    /api/auth/users/{id}/            # Update user
DELETE /api/auth/users/{id}/            # Delete user
```

## Thread APIs

### Thread Management

```
GET    /api/threads/                    # List all threads
POST   /api/threads/                    # Create new thread
GET    /api/threads/{id}/               # Get thread detail
PUT    /api/threads/{id}/               # Update thread
DELETE /api/threads/{id}/               # Delete thread
```

### Thread Feed

```
GET    /api/threads/feed/               # Get all threads feed
GET    /api/threads/following-feed/     # Get following users' threads feed
```

### Thread Interactions

```
POST   /api/threads/{id}/like/         # Like/unlike thread
POST   /api/threads/{id}/repost/        # Repost/unrepost thread
```

## Comment APIs

### Comment Management

```
GET    /api/threads/{thread_id}/comments/           # List comments
POST   /api/threads/{thread_id}/comments/           # Create comment
GET    /api/threads/{thread_id}/comments/{id}/      # Get comment detail
PUT    /api/threads/{thread_id}/comments/{id}/      # Update comment
DELETE /api/threads/{thread_id}/comments/{id}/      # Delete comment
```

### Comment Interactions

```
POST   /api/threads/{thread_id}/comments/{id}/like/    # Like/unlike comment
POST   /api/threads/{thread_id}/comments/{id}/repost/   # Repost/unrepost comment
```

## Follow APIs

### Follow Management

```
GET    /api/follows/                    # List follows
POST   /api/follows/                    # Create follow
DELETE /api/follows/{id}/               # Delete follow
```

## Notification APIs

### Notification Management

```
GET    /api/notifications/              # List notifications
GET    /api/notifications/unread-count/ # Get unread notifications count
POST   /api/notifications/{id}/mark-read/ # Mark notification as read
```

## Request/Response Examples

### Login

```json
POST /api/auth/users/login/
{
    "username": "user1",
    "password": "password123"
}
```

### Register

```json
POST /api/auth/users/
{
    "username": "newuser",
    "password": "password123",
    "password2": "password123",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Create Thread

```json
POST /api/threads/
{
    "content": "Thread content here"
}
```

### Create Comment

```json
POST /api/threads/{thread_id}/comments/
{
    "content": "Comment content here"
}
```

### Change Password

```json
POST /api/auth/users/change_password/
{
    "old_password": "oldpassword",
    "new_password": "newpassword",
    "new_password2": "newpassword"
}
```

## Authentication

- All endpoints except login and register require authentication
- Authentication is done using Django's session authentication
- Include credentials in requests (username/password)

## Pagination

- Most list endpoints support pagination
- Default page size: 7 items per page
- Use `?page=X` query parameter for pagination

## Error Responses

- 400 Bad Request: Invalid input data
- 401 Unauthorized: Not authenticated
- 403 Forbidden: Not authorized
- 404 Not Found: Resource not found
- 500 Internal Server Error: Server error

## Development Setup

1. Clone the repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Create config.py with required settings
5. Run migrations: `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run server: `python manage.py runserver`
