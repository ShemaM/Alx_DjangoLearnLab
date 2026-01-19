from django.db.models import Prefetch
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from .models import Book, Library


def list_books(request):
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})
