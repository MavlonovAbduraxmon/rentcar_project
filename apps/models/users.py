import re
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError
from django.db.models import (CharField, BigIntegerField, TextChoices, CASCADE, OneToOneField, DateField, TextField)
from apps.models.base import UUIDBaseModel
from apps.models.managers import CustomUserManager


class User(AbstractUser, UUIDBaseModel):
    class Type(TextChoices):
        SUPERUSER = 'superuser', 'Superuser'
        ADMIN = 'admin', 'Admin',
        USER = 'user', 'User'

    type = CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.USER
    )

    phone = CharField(max_length=13, unique=True, default="+998")
    email = None
    username = None
    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone'

    def check_phone(self):
        digits = re.findall(r'\d', self.phone)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        self.phone = phone.removeprefix('998')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class AdminProfile(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE)
    balance = BigIntegerField(default=0)
    telegram_id = BigIntegerField(null=True, blank=True)


class UserProfile(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE)
    birth_date = DateField()
    address = TextField()
    region = CharField(max_length=255)
    university = CharField(max_length=255)