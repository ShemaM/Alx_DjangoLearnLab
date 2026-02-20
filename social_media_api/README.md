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

- `POST /register` (or `/register/`) -> creates user and returns `{"token": "...", "user": {...}}`
- `POST /login` (or `/login/`) -> returns `{"token": "...", "user": {...}}`
- `GET /profile` (or `/profile/`) -> current user profile (requires auth)
- `PATCH /profile` (or `/profile/`) -> update current user (requires auth)

### Posts

CRUD (requires auth):

- `GET /posts/` -> list posts (paginated)
- `POST /posts/` -> create post (sets `author` from the token user)
- `GET /posts/<id>/` -> retrieve post
- `PATCH /posts/<id>/` -> update post (only the author)
- `DELETE /posts/<id>/` -> delete post (only the author)

Search (title/content):

- `GET /posts/?search=<query>`

Examples:

- Create post:
  - `POST /posts/`
  - Body:
    - `{"title": "My first post", "content": "Hello world"}`
- Search posts:
  - `GET /posts/?search=hello`

### Comments

CRUD (requires auth):

- `GET /comments/` -> list comments (paginated)
- `POST /comments/` -> create comment (sets `author` from the token user)
- `GET /comments/<id>/` -> retrieve comment
- `PATCH /comments/<id>/` -> update comment (only the author)
- `DELETE /comments/<id>/` -> delete comment (only the author)

Filter by post:

- `GET /comments/?post=<post_id>`

Examples:

- Create comment:
  - `POST /comments/`
  - Body:
    - `{"post": 1, "content": "Nice post!"}`
- List comments for a post:
  - `GET /comments/?post=1`

### Permissions

- Auth is required for all endpoints except `/register` and `/login`.
- Only the `author` can `PATCH`/`DELETE` their own posts/comments.

### Pagination

List endpoints are paginated (page size: 10):

- `GET /posts/?page=1`
- `GET /comments/?page=1`

Send the token in:

- `Authorization: Token <token>`
