from django.core.validators import FileExtensionValidator
from django.db.models import ImageField
from django.db.models.fields import CharField
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import CreatedBaseModel


class New(CreatedBaseModel):
    title = CharField(max_length=255)
    description =CKEditor5Field()
    image = ImageField(upload_to='news/%Y/%m/%d', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])

