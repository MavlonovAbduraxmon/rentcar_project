import re
from typing import Any

from django.contrib.auth import authenticate
from django.db.models import IntegerField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from apps.models import CarImage, Car, Category, User
from apps.models.cars import Brand
from apps.models.news import New
from apps.models.users import AdminProfile, UserProfile



class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image"]


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "logo"]


class NewSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = ["id", "title", "image", "description", "created_at"]


class CarImageSerializer(ModelSerializer):
    class Meta:
        model = CarImage
        fields = ["id", "image"]


class CarSerializer(ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = [
            "id", "name", "category", "brand", "price_day",
            "deposit", "limit_day", "fuel_type", "seats",
            "doors", "conditioner", "images", "description"
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "balance"]


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data["phone"],
            password=validated_data["password"]
        )
        return user

class SendSmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')

        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs):
        phone = attrs['phone']
        user, created = User.objects.get_or_create(phone=phone)
        user.set_unusable_password()

        return super().validate(attrs)


class LoginSerializer(Serializer):
    phone = CharField()
    code = CharField()


class AdminProfileSerializer(ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ["id", "user", "balance", "telegram_id"]


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "region", "address", "salary"]


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField(default=100100)
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs: dict[str, Any]):
        self.user = authenticate(phone=attrs['phone'], request=self.context['request'])

        if self.user is None:
            raise ValidationError(self.default_error_messages['no_active_account'])

        return attrs

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserProfileSerializer(self.user).data

        return {
            'message': "OK",
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)  # type: ignore
