from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from .models import Author, Book, Library, UserProfile


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
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


def role_check(role):
    return lambda u: u.is_authenticated and hasattr(u, 'userprofile') and u.userprofile.role == role


@user_passes_test(role_check(UserProfile.ADMIN), login_url='relationship_app:login')
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(role_check(UserProfile.LIBRARIAN), login_url='relationship_app:login')
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(role_check(UserProfile.MEMBER), login_url='relationship_app:login')
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')

        if not (title and title.strip() and author_id):
            return HttpResponse('Missing book data', status=400)

        author = get_object_or_404(Author, pk=author_id)
        Book.objects.create(title=title, author=author)
        return redirect('relationship_app:list_books')

    return HttpResponse('Add Book', status=200)


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author_id')

        updated = False
        if title and title != book.title:
            book.title = title
            updated = True
        if author_id:
            try:
                author_pk = int(author_id)
            except (TypeError, ValueError):
                return HttpResponse('Invalid author', status=400)
            if book.author_id != author_pk:
                book.author = get_object_or_404(Author, pk=author_pk)
                updated = True

        if not updated:
            return redirect('relationship_app:list_books')

        book.save()
        return redirect('relationship_app:list_books')

    return HttpResponse(f'Edit Book {book.pk}', status=200)


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('relationship_app:list_books')

    return HttpResponse(f'Delete Book {book.pk}', status=200)
