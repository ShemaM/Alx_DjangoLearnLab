## Automated tests

Run from repo root:

- `python social_media_api/manage.py test posts -v 2`
- `python social_media_api/manage.py test accounts -v 2`
- `python social_media_api/manage.py test notifications -v 2`

Current test suite:

- `posts.tests.PostsCommentsAPITests` (3 tests)
- `accounts.tests.FollowsAndFeedAPITests` (2 tests)
- `notifications.tests.NotificationsLikesAPITests` (4 tests)

Expected result:

- All tests pass (`OK`).
