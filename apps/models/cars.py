from django.db.models import ImageField, CASCADE, ForeignKey, ManyToManyField
from django.db.models.fields import CharField, IntegerField, TextField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class Category(UUIDBaseModel):
    name = CharField(max_length=120)
    image = ImageField(upload_to='categories/images/%Y/%m/%d')


class Brand(UUIDBaseModel):
    name = CharField(max_length=120)
    logo = ImageField(upload_to='logos/images/%Y/%m/%d')


class Car(CreatedBaseModel):
    name = CharField(max_length=255)
    category = ForeignKey('apps.Category', CASCADE, related_name="cars")
    brand = ForeignKey('apps.Brand', CASCADE, related_name="cars")
    deposit = IntegerField()
    limit_day = IntegerField()
    fuel_type = CharField(
        max_length=20,
        choices=[("electro", "Electro"), ("hybrid", "Hybrid"), ("gas", "Gas"), ("petrol", "Petrol")],
        default="gas"
    )
    description = CKEditor5Field(blank=True, null=True)
    features = ManyToManyField('apps.Feature', related_name="cars")
    color = ForeignKey('apps.Color', CASCADE, related_name="color")


class Color:
    color = CharField(max_length=255)

class CarImage(CreatedBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name="images")
    image = ImageField(upload_to='cars/images/%Y/%m/%d')


class CarRate(CreatedBaseModel):
    car = ForeignKey('apps.Car', CASCADE, related_name="rates")
    duration_label = CharField(max_length=50)
    min_duration = IntegerField()
    max_duration = IntegerField()
    price = IntegerField()

    class Meta:
        unique_together = ('car', 'min_duration', 'max_duration')
        ordering = ['min_duration']

    def __str__(self):
        return f"{self.car.name}: {self.duration_label} - {self.price} UZS"

class Feature(CreatedBaseModel):
    name = CharField(max_length=100, unique=True)
    icon_name = CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class FAQ(CreatedBaseModel):
    question = TextField(max_length=1000)
    answer = TextField(max_length=1000)