from django.urls import path

from .views import *

urlpatterns = [
    path('orders', OrderView.as_view(), name='orders'),
    path('orders/<int:order_id>', OrderDetailView.as_view(), name='order-detail'),
    path('orders/active', ActiveOrdersView.as_view(), name='active-orders'),
    path('orders/<int:order_id>/action', AcceptOrderView.as_view(), name='accept-order'),
]
