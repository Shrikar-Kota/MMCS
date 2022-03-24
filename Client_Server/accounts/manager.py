from lib2to3.pytree import Base
from multiprocessing.sharedctypes import Value
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("Username is required.")
        if not email:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("Password is required.")
        
        extra_fields.setdefault("token_creation_time", datetime.now(tz=timezone.utc))
        email = self.normalize_email(email)
        user = self.model(email = email, username = username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        extra_fields = {"is_staff": True, "is_superuser": True, "is_active": True}
        return self.create_user(username, email, password, **extra_fields)