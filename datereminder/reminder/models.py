from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, username, password):

        user = self.model(
            username=username
        )

        user.set_password(password)

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=200)

    objects = UserManager()

    USERNAME_FIELD = 'username'

class Person(models.Model):
    name = models.CharField(max_length=200)
    birthDay = models.DateField("person's birthday")
    relationship = models.CharField(max_length=200)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
