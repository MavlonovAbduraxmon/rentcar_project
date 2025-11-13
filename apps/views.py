from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView,
                                     RetrieveDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.filters import CarFilter
from apps.models import LongTermRental, UserProfile
from apps.models.cars import Brand, Car, Category
from apps.models.news import New
from apps.paginations import CustomCursorPagination
from apps.permissions import IsAdminOrReadOnly, IsRegisteredUser, IsAdminUser
from apps.serializers import (BrandModelSerializer, CarModelSerializer,
                              CategoryModelSerializer, NewModelSerializer, SendSmsCodeSerializer,
                              VerifySmsCodeSerializer, LongTermRentalModelSerializer,
                              VerifiedUserModelSerializer)
from apps.utils import send_code, random_code


@extend_schema(tags=['Auth'], summary="admin")
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        if not phone:
            return Response({"detail": "Telefon raqami kerak!"}, status=status.HTTP_400_BAD_REQUEST)

        code = random_code()
        valid, _ttl = send_code(phone, code)

        if valid:
            return Response({"detail": "SMS yuborildi!"})

        return Response(
            {"detail": f"Yana {int(_ttl)} soniyadan keyin yuborishingiz mumkin."},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )


@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = send_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)


@extend_schema(tags=['News'])
class NewsListCreateAPIView(ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewModelSerializer
    authentication_classes = ()


@extend_schema(tags=['News'])
class NewsModelViewSet(ModelViewSet):
    queryset = New.objects.all()
    serializer_class = NewModelSerializer
    authentication_classes = ()


@extend_schema_view(
    get=extend_schema(auth=[], description="List all categories (no token required)"),
    post=extend_schema(description="Create a new category (admin only)", summary="Admin"),
)
@extend_schema(tags=['Brand & Category'])
class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


@extend_schema(tags=['Brand & Category'])
class CategoryRetrieveAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    authentication_classes = ()
    lookup_field = 'name'


@extend_schema(tags=['Cars'])
class CarListCreateAPIView(ListCreateAPIView):
    queryset = Car.objects.filter(is_available=True)
    serializer_class = CarModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CarFilter
    search_fields = ['name', 'brand']
    authentication_classes = ()
    pagination_class = CustomCursorPagination


@extend_schema(tags=['Cars'])
class CarRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    authentication_classes = ()


@extend_schema(tags=['Brand & Category'])
class BrandListCreateAPIView(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    authentication_classes = ()


@extend_schema(tags=['Brand & Category'])
class BrandRetrieveAPIView(RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    authentication_classes = ()
    lookup_field = 'name'


class UserProfileCreateAPIView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = VerifiedUserModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Auth'])
class VerifyCodeAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = send_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)


@extend_schema(tags=['Rentals'])
class LongTermRentalRetrieveAPIView(RetrieveDestroyAPIView):
    queryset = LongTermRental.objects.all()
    serializer_class = LongTermRentalModelSerializer
    permission_classes = [IsAuthenticated, IsRegisteredUser]


@extend_schema(tags=['Rentals'])
class LongTermRentalListCreateAPIView(ListCreateAPIView):
    queryset = LongTermRental.objects.all()
    serializer_class = LongTermRentalModelSerializer
    permission_classes = [IsRegisteredUser]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            return ValidationError({"detail": "UserProfile is missing. Please complete profile first."})

        serializer.save(user=profile)


@extend_schema(tags=['Rentals'])
class LongTermRentalHistoryListAPIView(ListAPIView):
    queryset = LongTermRental.objects.all()
    serializer_class = LongTermRentalModelSerializer
    permission_classes = [IsRegisteredUser, IsAdminOrReadOnly]
