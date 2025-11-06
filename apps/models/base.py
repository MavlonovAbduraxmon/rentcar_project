from django.db.models import Func, Model
from django.db.models.fields import DateTimeField, UUIDField
from rest_framework.permissions import BasePermission


class GenRandomUUID(Func):
    function = "gen_random_uuid"
    template = "%(function)s()"  # no args
    output_field = UUIDField()


class UUIDBaseModel(Model):
    id = UUIDField(primary_key=True, db_default=GenRandomUUID(), editable=False)

    class Meta:
        abstract = True


class CreatedBaseModel(UUIDBaseModel):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_superuser

class IsRegisteredUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_registered