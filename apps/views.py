from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from apps.filters import CarFilter
from apps.models import Car, Category, CarImage, User
from apps.models.cars import Brand
from apps.models.news import New
from apps.serializers import CarSerializer, CategorySerializer, BrandSerializer, CarImageSerializer, NewSerializer, \
    UserSerializer, RegisterSerializer, LoginSerializer


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarFilter
    search_fields = ['name']


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class CarImageViewSet(ModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer


class NewsViewSet(ModelViewSet):
    queryset = New.objects.all().order_by('-created_at')
    serializer_class = NewSerializer


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AuthViewSet(ViewSet):
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered", "user_id": user.id}, status=status.HTTP_201_CREATED)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Login successful", "token": "jwt-token-here"})
