from django.urls import path

from .views import RestaurantMenuView

urlpatterns = [
    path('menu/', RestaurantMenuView.as_view(), name='categories'),
]
