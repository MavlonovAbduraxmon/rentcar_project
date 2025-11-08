from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.user.is_superuser

class IsRegisteredUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_registered