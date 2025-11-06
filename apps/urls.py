from django.urls import path
from apps.views import (BrandListCreateAPIView, CarListCreateAPIView,
                        CategoryListCreateAPIView, LoginAPIView,
                        NewsListCreateAPIView, SendCodeAPIView, CarRetrieveUpdateDestroyAPIView, VerifyCodeAPIView,
                        LongTermRentalHistoryListAPIView, UserProfileCreateAPIView)

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('auth/login', LoginAPIView.as_view(), name='login'),
    # path('user/register', UserProfileCreateAPIView.as_view(), name='user_profile'),
    path('news', NewsListCreateAPIView.as_view(), name='new-list'),
    path('categories', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('cars', CarListCreateAPIView.as_view(), name='car_model'),
    path('cars/<uuid:uuid>', CarRetrieveUpdateDestroyAPIView.as_view(), name='car_detail'),
    path('rentals/history', LongTermRentalHistoryListAPIView.as_view(), name='rents_history'),
    path('brands', BrandListCreateAPIView.as_view(), name='brand-list'),
]
