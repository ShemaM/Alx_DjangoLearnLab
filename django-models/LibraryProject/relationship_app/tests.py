from django.test import TestCase
from django.urls import reverse

from .models import Author, Book, Library


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
