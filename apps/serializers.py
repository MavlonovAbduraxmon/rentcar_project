import re
from typing import Any

from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField, HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import New, Brand, Car, Category, User, CarTariff, Feature, CarImage, LongTermRental, UserProfile
from apps.utils import check_phone


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image"]


class BrandModelSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "logo"]


class FeatureModelSerializer(ModelSerializer):
    class Meta:
        model = Feature
        fields = ['name', 'description', 'icon']


class NewModelSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = ["id", "title", "image", "description", "created_at"]


class CarModelSerializer(ModelSerializer):
    price = SerializerMethodField()
    features = FeatureModelSerializer(many=True)
    # carimages = CarImage(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['id', "name", 'price', 'deposit', 'limit_day', 'features']


    def get_price(self, obj):
        price = CarTariff.objects.filter(car=obj.id).first()
        return price.daily_price if price else None


class CarTariffModelSerializer(ModelSerializer):
    class Meta:
        model = CarTariff
        exclude = ['id', 'car', 'created_at', 'updated_at']


class CarImageModelSerializer(ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']


class CarDetailModelSerializer(ModelSerializer):
    brand = CharField(source='brand.name')
    price = CarTariffModelSerializer(many=True, source='price')
    features = FeatureModelSerializer(many=True)
    images = CarImageModelSerializer(many=True)
    similar_cars = SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'name', 'brand', 'price', 'features', 'similar_cars', 'images']
        lookup_fields = ['id', 'name']

    def get_similar_cars(self, obj):
        similar = Car.objects.filter(category=obj.category).exclude(id=obj.id)[:4]
        return CarModelSerializer(similar, many=True).data


class LongTermRentalModelSerializer(ModelSerializer):
    class Meta:
        model = LongTermRental
        exclude = ['user']


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone"]

class VerifiedUserModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserProfile
        exclude = ()


class RegisterModelSerializer(ModelSerializer):
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
    first_name = CharField(max_length=255, default='Alijon')
    last_name = CharField(max_length=255, default='Valiyev')
    password = PasswordField(max_length=255)

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone.removeprefix('998')


class LoginSerializer(Serializer):
    phone = CharField()
    code = CharField()


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
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token': str(refresh.access_token),
            'refresh token': str(refresh)
        }
        data = {
            'message': 'Valid Code',
            **tokens, **user_data
        }
        return data

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        is_valid = check_phone(**attrs)
        if not is_valid:
            raise ValidationError({'message': 'invalid or expired code'})
        phone = attrs['phone']

        self.user, _ = User.objects.get_or_create(phone=phone)
        attrs['user'] = self.user
        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)  # type: ignore
