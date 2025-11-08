from django.urls import path
from apps.views import (BrandListCreateAPIView,
                        CategoryListCreateAPIView, LoginAPIView,
                        NewsListCreateAPIView, SendCodeAPIView, CarRetrieveUpdateDestroyAPIView, VerifyCodeAPIView,
                        LongTermRentalHistoryListAPIView, LongTermRentalListCreateAPIView, CarListCreateAPIView)

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='send_code'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='verify_code'),
    path('news', NewsListCreateAPIView.as_view(), name='new-list'),
    path('categories', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('user/rentals', LongTermRentalListCreateAPIView.as_view(), name='rent_car'),
    path('cars/<uuid:uuid>', CarRetrieveUpdateDestroyAPIView.as_view(), name='car_detail'),
    path('cars', CarListCreateAPIView.as_view(), name='car_list'),
    path('rentals/history', LongTermRentalHistoryListAPIView.as_view(), name='rents_history'),
    path('brands', BrandListCreateAPIView.as_view(), name='brand-list'),
]
