from django.urls import path
from .views import RegisterAPIView, UserListAPIView, UserList, UserCreateAPIView
from . import views


urlpatterns = [
    path('users-list/', UserList.as_view(), name='user-list-data'),
    path('users-store/', UserCreateAPIView.as_view(), name='users-store'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('signin/', views.UserSignin.as_view(), name='signin'),
    
    # path('users/', UserListAPIView.as_view(), name='users'),
    
]
