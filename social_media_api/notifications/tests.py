from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from posts.models import Post

from .models import Notification

User = get_user_model()


class NotificationsLikesAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass12345")
        self.user2 = User.objects.create_user(username="user2", password="pass12345")
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

    def auth_as(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_like_creates_notification_and_prevents_duplicate(self):
        post = Post.objects.create(author=self.user2, title="Hello", content="World")

        self.auth_as(self.token1)
        resp1 = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(resp1.status_code, 201)

        resp2 = self.client.post(f"/api/posts/{post.id}/like/")
        self.assertEqual(resp2.status_code, 400)

        notif = Notification.objects.filter(recipient=self.user2, actor=self.user1).first()
        self.assertIsNotNone(notif)
        self.assertIn("liked", notif.verb.lower())

    def test_follow_creates_notification(self):
        self.auth_as(self.token1)
        resp = self.client.post(f"/api/follow/{self.user2.id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user2,
                actor=self.user1,
                verb__icontains="follow",
            ).exists()
        )

    def test_comment_creates_notification(self):
        post = Post.objects.create(author=self.user2, title="Hello", content="World")

        self.auth_as(self.token1)
        resp = self.client.post(
            "/api/comments/",
            {"post": post.id, "content": "Nice!"},
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(
            Notification.objects.filter(
                recipient=self.user2,
                actor=self.user1,
                verb__icontains="comment",
            ).exists()
        )

    def test_notifications_endpoint_lists_unread_first(self):
        post = Post.objects.create(author=self.user2, title="Hello", content="World")
        Notification.create(recipient=self.user2, actor=self.user1, verb="liked your post", target=post)
        read_notif = Notification.create(recipient=self.user2, actor=self.user1, verb="followed you")
        read_notif.is_read = True
        read_notif.save(update_fields=["is_read"])

        self.auth_as(self.token2)
        resp = self.client.get("/api/notifications/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["count"], 2)
        self.assertFalse(resp.data["results"][0]["is_read"])
