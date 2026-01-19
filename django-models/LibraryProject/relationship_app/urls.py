from django.urls import path

from .views import LibraryDetailView, list_books

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
