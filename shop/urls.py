from django.urls import path

from . import views

urlpatterns = [
    path('customers', views.CustomerListCreateAPIView.as_view(), name='api-customer-list'),
    path('customers/<int:pk>', views.CustomerDetailsAPIView.as_view(), name='api-customer-details'),
    path('orders', views.OrderListCreateAPIView.as_view(), name='api-order-list'),
    path('orders/<int:pk>', views.OrderDetailsAPIView.as_view(), name='api-order-details'),
    path('orders/customers/<int:customer_pk>', views.CreateOrderAPIView.as_view(), name='api-order-create'),
]