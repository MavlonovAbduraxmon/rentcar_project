from django.db.models import (CASCADE, BooleanField, ForeignKey, ImageField,
                              ManyToManyField, TextChoices, OneToOneField)
from django.db.models.fields import CharField, IntegerField, TextField, DateTimeField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from apps.models.base import CreatedBaseModel, UUIDBaseModel


class Category(UUIDBaseModel):
    name = CharField(max_length=120)
    image = ImageField(upload_to='categories/images/%Y/%m/%d')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

class Brand(UUIDBaseModel):
    name = CharField(max_length=120)
    logo = ImageField(upload_to='logos/images/%Y/%m/%d')

    def __str__(self):
        return self.name

class Car(CreatedBaseModel):
    class FuelType(TextChoices):
        GAS = 'gas', 'Gas'
        ELECTRIC = 'electric', 'Electric'
        HYBRID = 'hybrid', 'Hybrid'

    class TransmissionType(TextChoices):
        MANUAL = 'manual', 'Manual',
        AUTOMATIC = 'automatic', 'Automatic'

    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', CASCADE, related_name="category")
    brand = ForeignKey('apps.Brand', CASCADE, related_name="brand")
    deposit = IntegerField()
    limit_day = IntegerField()
    main_photo = ImageField(upload_to='main_images/')
    fuel_type = CharField(max_length=15, choices=FuelType.choices, default=FuelType.GAS)
    description = CKEditor5Field(blank=True, null=True)
    features = ManyToManyField('apps.Feature', related_name="Feature")
    color = ForeignKey('apps.CarColor', CASCADE, related_name="color")
    transmission_type = CharField(max_length=15, choices=TransmissionType.choices, default=TransmissionType.AUTOMATIC)
    is_available = BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")


class CarColor(CreatedBaseModel):
    name = CharField(max_length=155)

    def __str__(self):
        return self.name

class CarImage(CreatedBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name="images")
    image = ImageField(upload_to='cars/images/%Y/%m/%d')


class CarTariff(CreatedBaseModel):
    car = OneToOneField('apps.Car', CASCADE, related_name="tariff")
    daily_price = IntegerField()
    one_to_three_day = IntegerField()
    three_to_seven_day = IntegerField()
    seven_to_half_month = IntegerField()
    half_to_one_month = IntegerField()

    class Meta:
        verbose_name = _("CarTariff")
        verbose_name_plural = _("CarTariffs")


class Feature(CreatedBaseModel):
    icon = ImageField(upload_to='car/icons/features/%Y/%m/%d/')
    name = CharField(max_length=155)
    description = CKEditor5Field(max_length=155)

    def __str__(self):
        return self.name

class FAQ(CreatedBaseModel):
    question = TextField()
    answer = TextField()

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")


class Reviews(UUIDBaseModel):
    car = ForeignKey('apps.Car',CASCADE,related_name='reviews')
    user = ForeignKey('apps.User', CASCADE, related_name='reviews')
    stars = IntegerField()
    comment = CKEditor5Field()


class LongTermRental(CreatedBaseModel):
    class PaymentMethod(TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'

    car = ForeignKey('apps.Car', CASCADE, related_name='longtermrental')
    user = ForeignKey('apps.User', CASCADE, related_name='user')
    pick_up_location = CharField(max_length=255)
    pick_up_data_time = DateTimeField()
    drop_of_location = CharField(max_length=255)
    drop_of_data_time = DateTimeField()
    payment_method = CharField(max_length=4, choices=PaymentMethod.choices, default=PaymentMethod.CARD)

    class Meta:
        verbose_name = _("LongTermRental")
        verbose_name_plural = _("LongTermRentals")
