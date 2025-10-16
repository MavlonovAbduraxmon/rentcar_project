from django.urls import path
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.views import (BrandListCreateAPIView, CategoryListCreateAPIView,
                        LoginAPIView, NewsListCreateAPIView, SendCodeAPIView, CarListCreateAPIView)

TokenObtainPairView
urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('login', LoginAPIView.as_view(), name='register'),
    path('news', NewsListCreateAPIView.as_view(), name='new-list'),
    path('categories', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('car', CarListCreateAPIView.as_view(), name='car_model'),
    path('car/<uuid:uuid>', RetrieveUpdateDestroyAPIView.as_view(), name='car_detail'),
    path('brands', BrandListCreateAPIView.as_view(), name='brand-list'),
]