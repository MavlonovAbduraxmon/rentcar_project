import code
import re
from typing import Any
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, SerializerMethodField, HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework_simplejwt.tokens import RefreshToken, Token
from apps.models import New, Brand, Car, Category, User, CarTariff, Feature, CarImage, LongTermRental, UserProfile
from apps.utils import find_contact_type


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
    features = FeatureModelSerializer(many=True, read_only=True)
    # carimages = CarImage(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['id', "name", 'price', 'deposit', 'limit_day', 'features']


    def get_price(self, obj):
        price = CarTariff.objects.filter(car=obj).first()
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
    price = CarTariffModelSerializer(many=True, source='cartariff_set')
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


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField(default=100100)
    token_class = RefreshToken

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs: dict[str, Any]):
        phone_number = attrs['phone']

        try:
            user_obj = User.objects.get(phone=phone_number)

            authenticated_user = authenticate(phone=phone_number, request=self.context['request'])
            if authenticated_user is not None:
                self.user = authenticated_user
            else:
                if not user_obj.is_active:
                    raise ValidationError("Foydalanuvchi faol emas. Ma'muriyatga murojaat qiling.")
                self.user = user_obj

        except User.DoesNotExist:
            try:
                self.user = User.objects.create(phone=phone_number)
            except Exception as e:
                print(f"User yaratishda xato: {e}")
                raise ValidationError(
                    "Foydalanuvchini yaratishda kutilmagan xato yuz berdi. Iltimos, keyinroq urinib ko'ring.")

        if self.user is None or not self.user.is_active:
            raise ValidationError("Foydalanuvchini topish, yaratish yoki faollikni tekshirishda xato yuz berdi.")

        return attrs

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserModelSerializer(self.user).data

        return {
            'message': 'OK.',
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)


class LoginSerializer(Serializer):
    phone = CharField(max_length=255,default='901001010')
    code = CharField(max_length=50)
    token_class = RefreshToken
    user = None

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, phone):
        phone = find_contact_type(phone)
        return phone['value']

    def validate(self, attrs):
        phone = attrs['phone']

        try:
            self.user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise ValidationError(self.default_error_messages)

        if not self.user.check_password(code):
            raise ValidationError({"datail": 'Incorrect password'})
        return attrs

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token': str(refresh.access_token),
            'refresh token': str(refresh)
        }
        data = {
            'message': 'Valid Code',
            "data":{**tokens, **user_data}
        }
        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)  # type: ignore
