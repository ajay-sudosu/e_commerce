from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext as _
from django_countries.fields import CountryField


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, user_name, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff.")

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser.")

        return self.create_user(email, user_name, password, **kwargs)

    def create_user(self, email, user_name, password, **kwargs):
        if not email:
            raise ValueError(_('Must provide an email address.'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **kwargs)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email_address'), unique=True)
    user_name = models.CharField(max_length=150, blank=True)
    about = models.CharField(_('about'), max_length=150, blank=True)
    # delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=15, blank=True)
    postcode = models.CharField(max_length=12, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    address_line_2 = models.CharField(max_length=150, blank=True)
    # User_status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def __str__(self):
        return self.user_name
