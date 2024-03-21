from django.urls import path

from .views import *

urlpatterns = [
    path('orders', OrderView.as_view(), name='orders'),
    path('orders/<int:id>', OrderDetailView.as_view(), name='order-detail'),
]
