from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
  def create_user(self, first_name, last_name, email, username, password = None, is_staff = False, is_superuser = False):
    if not email:
      raise ValueError("Field `email` is required.")
    if not first_name:
      raise ValueError("Field `first_name` is required.")
    if not last_name:
      raise ValueError("Field `last_name` is required.")
    if not username:
      raise ValueError("Field `username` is required.")
    user = self.model(email = self.normalize_email(email))
    user.first_name = first_name
    user.last_name = last_name
    user.username = username
    user.set_password(password)
    user.is_active = True
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()
    return user

  def create_superuser(self, first_name, last_name, email, username, password):
    user = self.create_user(first_name = first_name, last_name = last_name, email = email, username = username, password = password, is_staff = True, is_superuser = True)
    user.save()
    return user

