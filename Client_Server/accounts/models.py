from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = models.CharField(max_length=14)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    signin_token = models.CharField(max_length=100, null=True, blank=True)
    account_verified = models.BooleanField(default=False)
    token_creation_time = models.DateTimeField()
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']