from django.db import models
from utils.base_model import BaseModel
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from .manager import UserManager
from django.utils import timezone


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    phoneNumber = PhoneNumberField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["phoneNumber", "name"]
    objects = UserManager()

    def __str__(self):
        return str(self.id)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


# Create your models here.
