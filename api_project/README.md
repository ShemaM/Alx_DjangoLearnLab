## API Project (DRF) - Authentication & Permissions

### Token authentication

This API uses **Django REST Framework TokenAuthentication**.

1. Add tables for token management:
   - `python manage.py migrate`
2. Create a user (and optionally an admin/staff user):
   - `python manage.py createsuperuser`

### Get a token

Send a POST request to:

- `POST /api/token/`

Body (form or JSON):

- `username`
- `password`

Example (PowerShell):

- `Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/token/ -Body @{ username="admin"; password="..." }`

Response:

- `{"token":"<your-token>"}`

### Use a token

Send the token in the `Authorization` header:

- `Authorization: Token <your-token>`

Example (PowerShell):

- `Invoke-RestMethod -Headers @{ Authorization = "Token <your-token>" } -Uri http://127.0.0.1:8000/api/books/`

### Permissions behavior

- All API endpoints require an authenticated user by default (see `api_project/settings.py`).
- `BookViewSet`:
  - Read (GET/HEAD/OPTIONS): any authenticated user
  - Write (POST/PUT/PATCH/DELETE): **staff/admin** users only
