from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager
    """
    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The specified user name must be set')

        if not email:
            raise ValueError('This email address must be set to')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    """

    class UserType(models.TextChoices):
        ADMIN = 'ADMIN', _('ADMIN')
        REGULAR = 'REGULAR', _('REGULAR')

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(validators=[validators.validate_email], unique=True, blank=False)
    first_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='User First Name')
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='User Last Name')
    user_type = models.CharField(max_length=25, choices=UserType.choices, default=UserType.REGULAR)
    user_company = models.ForeignKey('Company', null=True, blank=True, on_delete=models.CASCADE, related_name='user')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Company(models.Model):
    name = models.CharField(null=True, unique=True, blank=True, max_length=256)
    address = models.CharField(max_length=256, null=True, blank=True)
    owner = models.ForeignKey(CustomUser,
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE,
                              verbose_name='Company owner')

    def __str__(self):
        return f'company: {self.name}, owner: {self.owner.email}'

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['owner']


class Office(models.Model):
    name = models.CharField(max_length=256, unique=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    country = models.CharField(max_length=256, null=True, blank=True)
    region = models.CharField(max_length=256, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Office company')

    def __str__(self):
        return f'office: {self.name}, company:{self.company.name}'


class Vehicle(models.Model):
    pass

