from django.urls import path
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('signin', views.CreateOrderAPIView.UserLoginView),
    path('customers', views.CustomerListCreateAPIView.as_view(), name='api-customer-list'),
    path('customers/<int:pk>', views.CustomerDetailsAPIView.as_view(), name='api-customer-details'),
    path('orders', views.OrderListCreateAPIView.as_view(), name='api-order-list'),
    path('orders/<int:pk>', views.OrderDetailsAPIView.as_view(), name='api-order-details'),
    path('orders/customers/<int:customer_pk>', views.CreateOrderAPIView.as_view(), name='api-order-create'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('social/auth/', views.CreateOrderAPIView.social_login),

]
