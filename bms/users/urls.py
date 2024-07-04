from django.urls import path
from .views import Register, GetUsers


urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('users', GetUsers.as_view(), name='users'),
    path('users/<int:slug>', GetUsers.as_view(), name='user_detail'),
    # path('login', Login.as_view(), name='login'),
]