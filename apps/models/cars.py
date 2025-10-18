from django.db.models import (CASCADE, BooleanField, ForeignKey, ImageField,
                              ManyToManyField, TextChoices)
from django.db.models.fields import CharField, IntegerField, TextField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from rest_framework.fields import DateTimeField  # TODO fix

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class Category(UUIDBaseModel):
    name = CharField(max_length=120)
    image = ImageField(upload_to='categories/images/%Y/%m/%d')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Brand(UUIDBaseModel):
    name = CharField(max_length=120)
    logo = ImageField(upload_to='logos/images/%Y/%m/%d')


class Car(CreatedBaseModel):
    class FuelType(TextChoices):
        GAS = 'gas', 'Gas'
        ELECTRIC = 'electric', 'Electric'
        HYBRID = 'hybrid', 'Hybrid'

    class TransmissionType(TextChoices):
        MANUAL = 'manual', 'Manual',
        AUTOMATIC = 'automatic', 'Automatic'

    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', CASCADE, related_name="cars")
    brand = ForeignKey('apps.Brand', CASCADE, related_name="cars")
    deposit = IntegerField()
    limit_day = IntegerField()
    fuel_type = CharField(max_length=15, choices=FuelType.choices, default=FuelType.GAS)
    description = CKEditor5Field(blank=True, null=True)
    features = ManyToManyField('apps.Feature', related_name="cars")
    transmission_type = CharField(max_length=15, choices=TransmissionType.choices, default=TransmissionType.AUTOMATIC)
    tariff = ForeignKey('apps.CarTariff', CASCADE, related_name="cars")

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")


class CarColor(CreatedBaseModel):
    name = CharField(max_length=155)


class CarImage(CreatedBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name="images")
    image = ImageField(upload_to='cars/images/%Y/%m/%d')


class CarTariff(CreatedBaseModel):
    daily_price = IntegerField()
    one_to_three_day = IntegerField()
    three_to_seven_day = IntegerField()
    seven_to_half_month = IntegerField()
    half_to_one_month = IntegerField()

    class Meta:
        verbose_name = _("CarTariff")
        verbose_name_plural = _("CarTariffs")


class Feature(CreatedBaseModel):
    icon = ImageField()
    name = CharField(max_length=155)
    description = CKEditor5Field(max_length=155)


class FAQ(CreatedBaseModel):
    question = TextField()
    answer = TextField()

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")


class LongTermRental(CreatedBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name='longtermrental')
    user = ForeignKey('apps.User', CASCADE, related_name='user')
    start_data = DateTimeField()
    end_data = DateTimeField()
    total_price = IntegerField()
    is_paid = BooleanField(default=False)

    class Meta:
        verbose_name = _("LongTermRental")
        verbose_name_plural = _("LongTermRentals")
