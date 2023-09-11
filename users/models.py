from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password= None):
        if not email:
            raise ValueError('Please enter a valid email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self ,email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_staff =True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = UserAccountManager()
    
    USERNAME_FIELD = 'email'
    
    def __str__(self) -> str:
        return f'User Created Successfully{self.email}'
    
