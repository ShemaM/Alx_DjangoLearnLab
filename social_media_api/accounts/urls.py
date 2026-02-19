from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import LoginView, ProfileView, RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('register/', RegisterView.as_view()),
    path('login', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view()),
    path('token', obtain_auth_token, name='token'),
    path('token/', obtain_auth_token),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/', ProfileView.as_view()),
]
