erDiagram
    accounts_myuser {
        bigint id PK
        varchar bio
        varchar profile_picture
        int user_id FK
        varchar link
    }
    auth_group {
        int id PK
        varchar name
    }
    auth_group_permissions {
        bigint id PK
        int group_id FK
        int permission_id FK
    }
    auth_permission {
        int id PK
        varchar name
        int content_type_id FK
        varchar codename
    }
    auth_user {
        int id PK
        varchar password
        datetime last_login
        tinyint is_superuser
        varchar username
        varchar first_name
        varchar last_name
        varchar email
        tinyint is_staff
        tinyint is_active
        datetime date_joined
    }
    auth_user_groups {
        bigint id PK
        int user_id FK
        int group_id FK
    }
    auth_user_user_permissions {
        bigint id PK
        int user_id FK
        int permission_id FK
    }
    thread_comment {
        bigint id PK
        datetime created_at
        datetime updated_at
        bigint thread_id FK
        int user_id FK
        int comment_count
        int likes_count
        longtext content
        bigint parent_comment_id FK
    }
    thread_commentimage {
        bigint id PK
        varchar image
        bigint comment_id FK
    }
    thread_follow {
        bigint id PK
        datetime created_at
        datetime updated_at
        int followed_id FK
        int follower_id FK
    }
    thread_like {
        bigint id PK
        datetime created_at
        datetime updated_at
        bigint thread_id FK
        int user_id FK
    }
    thread_likecomment {
        bigint id PK
        datetime created_at
        datetime updated_at
        bigint comment_id FK
        int user_id FK
    }
    thread_notification {
        bigint id PK
        varchar type
        varchar content
        tinyint is_read
        datetime created_at
        int actioner_id FK
        int user_id FK
    }
    thread_repost {
        bigint id PK
        datetime created_at
        datetime updated_at
        bigint thread_id FK
        int user_id FK
    }
    thread_repostcomment {
        bigint id PK
        datetime created_at
        datetime updated_at
        bigint comment_id FK
        int user_id FK
    }
    thread_thread {
        bigint id PK
        int likes_count
        int comment_count
        datetime created_at
        datetime updated_at
        int user_id FK
        longtext content
    }
    thread_threadimage {
        bigint id PK
        varchar image
        bigint thread_id FK
    }

    accounts_myuser ||--o| auth_user : "user_id"
    auth_group_permissions }o--|| auth_group : "group_id"
    auth_group_permissions }o--|| auth_permission : "permission_id"
    auth_permission ||--o| django_content_type : "content_type_id"
    auth_user_groups }o--|| auth_user : "user_id"
    auth_user_groups }o--|| auth_group : "group_id"
    auth_user_user_permissions }o--|| auth_user : "user_id"
    auth_user_user_permissions }o--|| auth_permission : "permission_id"
    thread_comment ||--o| thread_thread : "thread_id"
    thread_comment ||--o| auth_user : "user_id"
    thread_comment ||--o| thread_comment : "parent_comment_id"
    thread_commentimage ||--o| thread_comment : "comment_id"
    thread_follow ||--o| auth_user : "followed_id"
    thread_follow ||--o| auth_user : "follower_id"
    thread_like ||--o| thread_thread : "thread_id"
    thread_like ||--o| auth_user : "user_id"
    thread_likecomment ||--o| thread_comment : "comment_id"
    thread_likecomment ||--o| auth_user : "user_id"
    thread_notification ||--o| auth_user : "actioner_id"
    thread_notification ||--o| auth_user : "user_id"
    thread_repost ||--o| thread_thread : "thread_id"
    thread_repost ||--o| auth_user : "user_id"
    thread_repostcomment ||--o| thread_comment : "comment_id"
    thread_repostcomment ||--o| auth_user : "user_id"
    thread_thread ||--o| auth_user : "user_id"
    thread_threadimage ||--o| thread_thread : "thread_id"
