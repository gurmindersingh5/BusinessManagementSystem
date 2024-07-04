from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from .manager import UserManager
from django.utils import timezone


class Users(AbstractBaseUser):
    """
    Defines Schema for User Model
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=True, null=True)
    # password = models....... not required because AbstractBaseUser class already includes a password field
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_employee = models.BooleanField(default=True)
    created_at = models.DateField(default=timezone.now)

    objects = UserManager()
    
    USERNAME_FIELD = 'username' # USERNAME_FIELD is unique identifier for user
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
