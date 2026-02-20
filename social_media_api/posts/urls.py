from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FeedView, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
    path('', include(router.urls)),
]
