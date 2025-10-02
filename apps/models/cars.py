from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import FileExtensionValidator
from django.db.models import ImageField, CASCADE, ForeignKey
from django.db.models.fields import CharField, IntegerField, PositiveIntegerField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class Category(UUIDBaseModel):
    name = CharField(max_length=120)


class Car(CreatedBaseModel):
    name = CharField(max_length=255)
    price = IntegerField()
    image = ImageField(upload_to='cars/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    description = CKEditor5Field()
    deposit = IntegerField()
    category = ForeignKey('apps.Category', CASCADE)


class CarImage(CreatedBaseModel):
    image = ImageField(upload_to='images/')
    content_type = ForeignKey('contenttypes.ContentType', CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')