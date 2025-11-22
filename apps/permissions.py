from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework_simplejwt.authentication import JWTAuthentication


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_admin
        )


class IsRegisteredUser(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            raise AuthenticationFailed('Tizimga kirish kerak')
        from apps.models import UserProfile
        try:
            UserProfile.objects.get(user=request.user)
            return True
        except:
            raise PermissionDenied('Avval ro\'yxatdan o\'ting')


class IsGetOrLocked(BaseAuthentication):
    def __init__(self):
        self.base_auth = JWTAuthentication()

    def authenticate(self, request):
        view = getattr(request, "parser_context", {}).get("view", None)
        action = getattr(view, "action", None)

        if request.method == "GET" and action in ["list", "retrieve"]:
            return None
        return self.base_auth.authenticate(request)


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            raise AuthenticationFailed('Token kerak')
        return True


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            raise AuthenticationFailed('Token kerak')

        if not request.user.is_staff:
            raise PermissionDenied('Faqat admin')

        return True
