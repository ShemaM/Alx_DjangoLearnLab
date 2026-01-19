from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import DetailView

from .models import Book


def list_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = 'relationship_app.Library'
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'