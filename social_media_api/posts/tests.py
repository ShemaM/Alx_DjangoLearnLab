from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Comment, Post

User = get_user_model()


class PostsCommentsAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass12345')
        self.user2 = User.objects.create_user(username='user2', password='pass12345')
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

    def auth_as(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_post_crud_and_permissions(self):
        self.auth_as(self.token1)
        create_resp = self.client.post(
            '/posts/',
            {'title': 'Hello', 'content': 'World'},
            format='json',
        )
        self.assertEqual(create_resp.status_code, 201)
        post_id = create_resp.data['id']

        self.auth_as(self.token2)
        patch_resp = self.client.patch(f'/posts/{post_id}/', {'title': 'Nope'}, format='json')
        self.assertEqual(patch_resp.status_code, 403)

        self.auth_as(self.token1)
        list_resp = self.client.get('/posts/')
        self.assertEqual(list_resp.status_code, 200)
        self.assertIn('results', list_resp.data)

    def test_post_search(self):
        Post.objects.create(author=self.user1, title='Django', content='REST framework')
        Post.objects.create(author=self.user1, title='Cooking', content='Recipes')

        self.auth_as(self.token1)
        resp = self.client.get('/posts/?search=django')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['count'], 1)

    def test_comment_crud_and_filtering(self):
        post = Post.objects.create(author=self.user1, title='Post', content='Content')
        self.auth_as(self.token1)

        create_resp = self.client.post(
            '/comments/',
            {'post': post.id, 'content': 'Nice post'},
            format='json',
        )
        self.assertEqual(create_resp.status_code, 201)
        comment_id = create_resp.data['id']

        self.auth_as(self.token2)
        delete_resp = self.client.delete(f'/comments/{comment_id}/')
        self.assertEqual(delete_resp.status_code, 403)

        self.auth_as(self.token1)
        list_resp = self.client.get(f'/comments/?post={post.id}')
        self.assertEqual(list_resp.status_code, 200)
        self.assertIn('results', list_resp.data)
        self.assertEqual(list_resp.data['count'], 1)

