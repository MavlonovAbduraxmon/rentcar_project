import re
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import ValidationError
from django.db.models import (CharField, TextChoices)

from apps.models.base import UUIDBaseModel
from apps.models.managers import CustomUserManager


class User(AbstractUser, UUIDBaseModel):
    class Type(TextChoices):
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

    def get_formatted_phone(self):
        if self.phone and len(self.phone) >= 12 and self.phone.startswith('998'):
            num = self.phone.lstrip('+').replace(' ', '')
            return f'+{num[:3]}({num[3:5]}) {num[5:8]}-{num[8:10]}-{num[10:]}'
        return self.phone

    def __str__(self):
        return self.get_formatted_phone()

    def check_phone(self):
        digits = re.findall(r'\d', self.phone)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        self.phone = phone.removeprefix('998')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.check_phone()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)



