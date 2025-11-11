from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_superuser

class IsRegisteredUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_admin:
            return request.user.is_authenticated

# utils/permissions.py
from rest_framework.permissions import AllowAny, IsAdminUser

class ReadAnyCreateAdminMixin:
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]
