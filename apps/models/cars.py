from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import FileExtensionValidator
from django.db.models import ImageField, CASCADE, ForeignKey, BooleanField
from django.db.models.fields import CharField, IntegerField, PositiveIntegerField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class Category(UUIDBaseModel):
    name = CharField(max_length=120)


class Brand(UUIDBaseModel):
    name = CharField(max_length=120)


class Car(CreatedBaseModel):
    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', CASCADE, related_name="cars")
    brand = ForeignKey('apps.Brand', CASCADE, related_name="cars")
    # price_day = IntegerField()
    deposit = IntegerField()
    limit_day = IntegerField()
    fuel_type = CharField(
        max_length=20,
        choices=[("electro", "Electro"), ("hybrid", "Hybrid"), ("gas", "Gas"), ("petrol", "Petrol")],
        default="gas"
    )
    # seats = IntegerField(default=4)
    # doors = IntegerField(default=4)
    # conditioner = BooleanField(default=True)
    # image = ImageField(upload_to='cars/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    description = CKEditor5Field(blank=True, null=True)


class CarImage(CreatedBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name="images")
    image = ImageField(upload_to='cars/images/%Y/%m/%d')
