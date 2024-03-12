from django.urls import path

from .views import *

urlpatterns = [
    path('register/', CourierSignUpView.as_view(), name='courier-register'),
    path('login/', CourierSignInView.as_view(), name='courier-login'),
    path('logout/', CourierSignOutView.as_view(), name='courier-logout'),
    path('profile/<slug:slug>', CourierProfileView.as_view(), name='courier-profile'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:id>', OrderDetailView.as_view(), name='cart-detail'),
]
