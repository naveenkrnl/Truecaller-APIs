from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator


class MyUserManager(BaseUserManager):
    def create_user(self, name, phone_number, email, password=None):
        """
        Creates and saves a User with the given phone number, name and password
        """
        if not phone_number:
            raise ValueError('User must have a Phone Number')
        if not email:
            email=""
        else:
            email=self.normalize_email(email),

        user = self.model(
            name=name,
            phone_number=phone_number,
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone_number, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        email=""
        user = self.create_user(
            name, 
            phone_number,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

NAME_REGEX='^[a-zA-Z]*$'
PHONENO_REGEX='^[0-9]*{10}$'

#  overriding default USER MODEL
class MyUser(AbstractBaseUser):
    name=models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20,
        unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        null=True,
        blank=True
    )
    spam_count = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True