from django.urls import path

from .views import RestaurantView

urlpatterns = [
    path('', RestaurantView.as_view(), name='categories')
]
