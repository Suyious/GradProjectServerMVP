from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager

class User(AbstractUser, PermissionsMixin):
  first_name = models.CharField(verbose_name="First Name", max_length=255)
  last_name = models.CharField(verbose_name="Last Name", max_length=255)
  email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
  password = models.CharField(max_length=255)
  username = models.CharField(max_length=255, unique=True)

  objects = UserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS =  ["first_name", "last_name", "username"]

  def __str__(self):
    return self.email

  def token(self):
    refresh = RefreshToken.for_user(self)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
