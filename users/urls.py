from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView
urlpatterns = [
    path('/register', UserRegistrationAPIView.as_view(), name='user-register'),
    path('/login', UserLoginAPIView.as_view(), name='user-login'),
]