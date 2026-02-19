from rest_framework import generics, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated, SAFE_METHODS

from .models import Book
from .serializers import BookSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]


class IsAdminOrReadOnlyAuthenticated(BasePermission):
    """
    - Read-only requests require an authenticated user.
    - Write requests require an admin/staff user.
    """

    def has_permission(self, request, view):
        user = request.user
        if request.method in SAFE_METHODS:
            return bool(user and user.is_authenticated)
        return bool(user and user.is_staff)


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnlyAuthenticated]
