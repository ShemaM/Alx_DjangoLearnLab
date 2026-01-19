from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Library, UserProfile


class RelationshipAppViewsTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Author One')
        self.book = Book.objects.create(title='Book One', author=self.author)
        self.library = Library.objects.create(name='Central Library')
        self.library.books.add(self.book)

    def test_list_books_view_displays_books(self):
        url = reverse('relationship_app:list_books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.author.name)

    def test_list_books_view_selects_authors(self):
        url = reverse('relationship_app:list_books')
        response = self.client.get(url)

        books = response.context['books']
        self.assertIn('author', books.query.select_related)

    def test_library_detail_view_displays_library_and_books(self):
        url = reverse('relationship_app:library_detail', args=[self.library.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.library.name)
        self.assertContains(response, self.book.title)


class RoleAccessControlTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='pass123')
        self.admin_user.userprofile.role = UserProfile.ADMIN
        self.admin_user.userprofile.save()

        self.librarian_user = User.objects.create_user(username='librarian', password='pass123')
        self.librarian_user.userprofile.role = UserProfile.LIBRARIAN
        self.librarian_user.userprofile.save()

        self.member_user = User.objects.create_user(username='member', password='pass123')
        # Member role is default

    def test_user_profile_created_on_user_creation(self):
        new_user = User.objects.create_user(username='newuser', password='pass123')
        self.assertTrue(hasattr(new_user, 'userprofile'))
        self.assertEqual(new_user.userprofile.role, UserProfile.MEMBER)

    def test_admin_view_requires_admin_role(self):
        self.client.login(username='admin', password='pass123')
        response = self.client.get(reverse('relationship_app:admin_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Admin Dashboard')

    def test_admin_view_redirects_non_admin(self):
        self.client.login(username='member', password='pass123')
        response = self.client.get(reverse('relationship_app:admin_view'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('relationship_app:login'), response.url)

    def test_librarian_and_member_views_respect_roles(self):
        self.client.login(username='librarian', password='pass123')
        librarian_response = self.client.get(reverse('relationship_app:librarian_view'))
        self.assertEqual(librarian_response.status_code, 200)
        self.assertContains(librarian_response, 'Librarian Area')

        self.client.logout()
        self.client.login(username='member', password='pass123')
        member_response = self.client.get(reverse('relationship_app:member_view'))
        self.assertEqual(member_response.status_code, 200)
        self.assertContains(member_response, 'Member Area')


class BookPermissionTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Author Two')
        self.book = Book.objects.create(title='Protected Book', author=self.author)
        self.user = User.objects.create_user(username='user1', password='pass123')

    def test_custom_permissions_defined_on_book(self):
        permissions = dict(Book._meta.permissions)
        self.assertIn('can_add_book', permissions)
        self.assertIn('can_change_book', permissions)
        self.assertIn('can_delete_book', permissions)

    def test_add_book_requires_permission(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('relationship_app:add_book'))
        self.assertEqual(response.status_code, 403)

    def test_add_book_allowed_with_permission(self):
        perm = Permission.objects.get(codename='can_add_book')
        self.user.user_permissions.add(perm)
        self.client.login(username='user1', password='pass123')

        get_response = self.client.get(reverse('relationship_app:add_book'))
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(
            reverse('relationship_app:add_book'),
            {'title': 'New Book', 'author_id': self.author.id},
        )
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_edit_and_delete_require_permissions(self):
        self.client.login(username='user1', password='pass123')
        edit_response = self.client.get(reverse('relationship_app:edit_book', args=[self.book.pk]))
        delete_response = self.client.get(reverse('relationship_app:delete_book', args=[self.book.pk]))
        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

    def test_edit_and_delete_allowed_with_permissions(self):
        change_perm = Permission.objects.get(codename='can_change_book')
        delete_perm = Permission.objects.get(codename='can_delete_book')
        self.user.user_permissions.add(change_perm, delete_perm)
        self.client.login(username='user1', password='pass123')

        edit_response = self.client.post(
            reverse('relationship_app:edit_book', args=[self.book.pk]),
            {'title': 'Updated Title', 'author_id': self.author.id},
        )
        self.assertEqual(edit_response.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

        delete_response = self.client.post(reverse('relationship_app:delete_book', args=[self.book.pk]))
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
