from django.db.models import Prefetch
from django.shortcuts import render
from django.views.generic import DetailView

from .models import Book, Library


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        return Library.objects.prefetch_related(
            Prefetch('books', queryset=Book.objects.select_related('author'), to_attr='prefetched_books')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = getattr(
            self.object,
            'prefetched_books',
            self.object.books.select_related('author').all(),
        )
        return context
