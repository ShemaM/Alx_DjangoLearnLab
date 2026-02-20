from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from posts.models import Post

User = get_user_model()


class FollowsAndFeedAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass12345")
        self.user2 = User.objects.create_user(username="user2", password="pass12345")
        self.user3 = User.objects.create_user(username="user3", password="pass12345")
        self.token1 = Token.objects.create(user=self.user1)

    def auth_as(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_follow_and_unfollow(self):
        self.auth_as(self.token1)

        follow_resp = self.client.post(f"/api/follow/{self.user2.id}/")
        self.assertEqual(follow_resp.status_code, 200)
        self.assertTrue(self.user1.following.filter(pk=self.user2.pk).exists())
        self.assertTrue(self.user2.followers.filter(pk=self.user1.pk).exists())

        unfollow_resp = self.client.post(f"/api/unfollow/{self.user2.id}/")
        self.assertEqual(unfollow_resp.status_code, 200)
        self.assertFalse(self.user1.following.filter(pk=self.user2.pk).exists())
        self.assertFalse(self.user2.followers.filter(pk=self.user1.pk).exists())

    def test_feed_contains_only_followed_users_posts(self):
        Post.objects.create(author=self.user2, title="From user2", content="hello")
        Post.objects.create(author=self.user3, title="From user3", content="nope")

        self.auth_as(self.token1)
        self.client.post(f"/api/follow/{self.user2.id}/")

        feed_resp = self.client.get("/api/feed/")
        self.assertEqual(feed_resp.status_code, 200)
        self.assertEqual(feed_resp.data["count"], 1)
        self.assertEqual(feed_resp.data["results"][0]["author"], self.user2.id)
