from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, Serializer
from apps.models import CarImage, Car, Category, User
from apps.models.cars import Brand
from apps.models.news import New
from apps.models.users import AdminProfile, UserProfile


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


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
