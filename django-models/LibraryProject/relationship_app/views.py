from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import DetailView

from .models import Book, Library, UserProfile


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
