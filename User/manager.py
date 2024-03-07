from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q


class UserManager(BaseUserManager):

    def create_user(self, username, id, phoneNumber, password=None):
        if not phoneNumber:
            raise ValueError("The Mobile Number field must be set")
        user = self.model(
            id=id,
            phoneNumber=phoneNumber,
            username=username
        )
        user.set_password(password)
        # user.headId = user
        user.save(using=self._db)

        return user

    def create_superuser(self, username, id, phoneNumber,  password=None):
        user = self.create_user(
            id=id,
            phoneNumber=phoneNumber,
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user



