from django.urls import path
from .views import RegisterAPIView, UserListAPIView
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
]
