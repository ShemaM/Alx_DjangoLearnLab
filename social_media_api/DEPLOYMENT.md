## Production deployment (example: Render)

This project supports environment-based production settings (see `social_media_api/settings.py`).

### Required environment variables

- `DJANGO_ENV=production`
- `DJANGO_DEBUG=False`
- `DJANGO_SECRET_KEY=<random secret>`
- `DJANGO_ALLOWED_HOSTS=<comma-separated hosts>` (e.g. `myapp.onrender.com`)
- `DJANGO_CSRF_TRUSTED_ORIGINS=<comma-separated origins>` (e.g. `https://myapp.onrender.com`)
- `DATABASE_URL=<postgres connection string>` (recommended)

### Render setup

Create a new **Web Service** from your GitHub repo:

- Root directory: `social_media_api`
- Build command:
  - `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start command:
  - `gunicorn social_media_api.wsgi:application --bind 0.0.0.0:$PORT`

### Final checks

- Run tests locally: `python manage.py test accounts posts notifications -v 2`
- Confirm endpoints:
  - `GET /api/feed/`
  - `POST /api/posts/<id>/like/`
  - `GET /api/notifications/`
