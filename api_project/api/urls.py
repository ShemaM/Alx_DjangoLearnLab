from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookList, BookViewSet, CustomObtainAuthToken

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Token retrieval: POST username/password -> {"token": "..."}
    path('token/', CustomObtainAuthToken.as_view(), name='api-token'),
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
]
