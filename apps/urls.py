from django.urls import path

from apps.views import (BrandListCreateAPIView, CarListCreateAPIView,
                        CategoryListCreateAPIView, LoginAPIView,
                        NewsListCreateAPIView, SendCodeAPIView, CarRetrieveUpdateDestroyAPIView, VerifyCodeAPIView)

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', VerifyCodeAPIView.as_view(), name='token_obtain_pair'),
    path('login', LoginAPIView.as_view(), name='register'),
    path('news', NewsListCreateAPIView.as_view(), name='new-list'),
    path('categories', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('cars', CarListCreateAPIView.as_view(), name='car_model'),
    path('cars/<uuid:uuid>', CarRetrieveUpdateDestroyAPIView.as_view(), name='car_detail'),
    path('brands', BrandListCreateAPIView.as_view(), name='brand-list'),

]
