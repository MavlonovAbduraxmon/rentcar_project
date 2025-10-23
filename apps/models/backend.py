from django.contrib.auth.backends import BaseBackend
from apps.models import User


class NoPasswordAuthBackend(BaseBackend):
    def authenticate(self, request, phone=None, **kwargs):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None