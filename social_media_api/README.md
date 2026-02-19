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

Send the token in:

- `Authorization: Token <token>`
