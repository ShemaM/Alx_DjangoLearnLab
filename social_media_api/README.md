## Social Media API (Django + DRF)

### Setup

- Install deps: `pip install django djangorestframework`
- From repo root:
  - `python social_media_api/manage.py migrate`
  - `python social_media_api/manage.py runserver`

### Custom user model

The `accounts.User` model extends `AbstractUser` and adds:

- `bio` (text)
- `profile_picture` (image upload)
- `followers` (many-to-many to self, `symmetrical=False`)

### Authentication (Token)

This API uses DRF TokenAuthentication (`rest_framework.authtoken`).

### Endpoints

- `POST /api/register` (or `/api/register/`) -> creates user and returns `{"token": "...", "user": {...}}`
- `POST /api/login` (or `/api/login/`) -> returns `{"token": "...", "user": {...}}`
- `GET /api/profile` (or `/api/profile/`) -> current user profile (requires auth)
- `PATCH /api/profile` (or `/api/profile/`) -> update current user (requires auth)

### Posts

CRUD (read-only without auth; write requires auth):

- `GET /api/posts/` -> list posts (paginated)
- `POST /api/posts/` -> create post (sets `author` from the token user)
- `GET /api/posts/<id>/` -> retrieve post
- `PATCH /api/posts/<id>/` -> update post (only the author)
- `DELETE /api/posts/<id>/` -> delete post (only the author)

Search (title/content):

- `GET /api/posts/?search=<query>`

Examples:

- Create post:
  - `POST /api/posts/`
  - Body:
    - `{"title": "My first post", "content": "Hello world"}`
- Search posts:
  - `GET /api/posts/?search=hello`

### Comments

CRUD (read-only without auth; write requires auth):

- `GET /api/comments/` -> list comments (paginated)
- `POST /api/comments/` -> create comment (sets `author` from the token user)
- `GET /api/comments/<id>/` -> retrieve comment
- `PATCH /api/comments/<id>/` -> update comment (only the author)
- `DELETE /api/comments/<id>/` -> delete comment (only the author)

Filter by post:

- `GET /api/comments/?post=<post_id>`

Examples:

- Create comment:
  - `POST /api/comments/`
  - Body:
    - `{"post": 1, "content": "Nice post!"}`
- List comments for a post:
  - `GET /api/comments/?post=1`

### Permissions

- Auth is required for all write operations, and for `/api/profile`.
- Only the `author` can `PATCH`/`DELETE` their own posts/comments.

### Pagination

List endpoints are paginated (page size: 10):

- `GET /api/posts/?page=1`
- `GET /api/comments/?page=1`

Send the token in:

- `Authorization: Token <token>`
