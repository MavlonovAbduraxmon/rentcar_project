import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db.models import (CharField, BigIntegerField, TextChoices, CASCADE, OneToOneField, DateField, BooleanField)
from rest_framework.exceptions import ValidationError
from apps.models.base import UUIDBaseModel
from apps.models.managers import CustomUserManager


class User(AbstractUser, UUIDBaseModel):
    class Type(TextChoices):
        ADMIN = 'admin', 'Admin',
        USER = 'user', 'User'

    phone = CharField(max_length=13, unique=True, default="+998")
    type = CharField(max_length=15, choices=Type.choices, default=Type.USER)
    is_registered = BooleanField(default=False)
    email = None
    username = None
    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'phone'

    @property
    def is_admin(self):
        return self.type == self.Type.ADMIN or self.is_superuser

    def check_phone(self):
        digits = re.findall(r'\d', self.phone)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        self.phone = phone.removeprefix('998')

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_superuser:
            self.type = self.Type.ADMIN

        if self.pk:
            old = User.objects.filter(pk=self.pk).first()
            if old and self.password != old.password:
                self.password = make_password(self.password)

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


class AdminProfile(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE)
    balance = BigIntegerField(default=0)
    telegram_id = BigIntegerField(null=True, blank=True)


class UserProfile(UUIDBaseModel):
    user = OneToOneField('apps.User', CASCADE, related_name='profile')
    data_of_birth = DateField()
    driver_licence_date_of_issue = DateField()
    id_card_number = CharField(max_length=9)
    personal_number = CharField(max_length=14)
    driver_licence_number = CharField(max_length=9)

    class Meta:
        verbose_name = 'Registered user'
        verbose_name_plural = 'Registered users'

    def save(self, *, force_insert=False, force_update=False, using=None, update_fields=None):
        self.user.is_registered = True
        self.user.save(update_fields=['is_registered'])
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return self.first_name + " " + self.last_name