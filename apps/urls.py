from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.views import SendCodeAPIView, LoginAPIView, CustomTokenRefreshView, NewsListCreateAPIView, \
    CategoryListCreateAPIView, CarImageListCreateAPIView, BrandListCreateAPIView

TokenObtainPairView
urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginAPIView.as_view(), name='register'),
    path('news', NewsListCreateAPIView.as_view(), name='new-list'),
    path('categories', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('cars', CarImageListCreateAPIView.as_view(), name='car-list'),
    path('brands', BrandListCreateAPIView.as_view(), name='brand-list'),
]