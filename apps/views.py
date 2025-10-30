from random import randint

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, RetrieveAPIView)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.filters import CarFilter
from apps.models import User
from apps.models.cars import Brand, Car, Category
from apps.models.news import New
from apps.serializers import (BrandModelSerializer, CarModelSerializer,
                              CategoryModelSerializer, LoginSerializer,
                              NewModelSerializer, RegisterModelSerializer,
                              SendSmsCodeSerializer, UserModelSerializer,
                              VerifySmsCodeSerializer)
from apps.utils import send_code


@extend_schema(tags=['Auth'])
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        code = randint(100_000, 999_999)
        send_code(phone, code)
        return Response({"message": "send sms code"})


@extend_schema(tags=['Auth'])
class LoginAPIView(TokenObtainPairView):
    serializer_class = VerifySmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = send_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)


@extend_schema(tags=['News'])
class NewsListCreateAPIView(ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewModelSerializer


@extend_schema(tags=['Brand & Category'])
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['Brand & Category'])
class CategoryRetrieveAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


@extend_schema(tags=['Cars'])
class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarFilter
    search_fields = ['name', 'brand']

    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)


@extend_schema(tags=['Cars'])
class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer


@extend_schema(tags=['Brand & Category'])
class BrandListCreateAPIView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer


@extend_schema(tags=['Brand & Category'])
class BrandRetrieveAPIView(RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer


class UserListAPIView(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class AuthListAPIView(ListAPIView):
    def register(self, request):
        serializer = RegisterModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered", "user_id": user.id}, status=status.HTTP_201_CREATED)

    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Login successful", "token": "jwt-token-here"})


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarFilter
    search_fields = ["name"]


@extend_schema(tags=['Auth'])
class VerifyCodeAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())
