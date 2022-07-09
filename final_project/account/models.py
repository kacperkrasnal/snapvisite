from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('confirm', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )
        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        if not user_name:
            raise ValueError("Users must have an username.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            user_name=user_name,
            **other_fields)
        user.set_password(password)
        user.save()
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    """
    Standard User model changed into this one,
    User have to log by email.
    """
    email = models.EmailField(verbose_name='email', max_length=80, unique=True)
    user_name = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    data_joined = models.DateTimeField(verbose_name='data joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last_login", auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True, null=True)
    # It's sending mail to confirm email.
    confirm = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.email}"
