from django.urls import path
from .views import Register, GetUsers

urlpatterns = [
    path('register', Register.as_view(), name='register'),
    path('users', GetUsers.as_view(), name='users'),
]