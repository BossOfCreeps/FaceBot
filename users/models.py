from random import choice
from string import ascii_lowercase

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True):
        user = self.model(email=self.normalize_email(email), )

        user.set_password(password)
        user.is_active = is_active
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    session_token = models.CharField(max_length=10, default=0)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    activation_token = models.CharField(max_length=50, default=''.join(choice(ascii_lowercase) for i in range(50)))

    objects = UserManager()

    class Meta:
        verbose_name = verbose_name_plural = "Пользователь"
