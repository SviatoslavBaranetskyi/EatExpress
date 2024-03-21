from django.urls import path

from .views import SignUpView, SignInView, SignOutView, ProfileView

urlpatterns = [
    path('register', SignUpView.as_view(), name='user-register'),
    path('login', SignInView.as_view(), name='user-login'),
    path('logout', SignOutView.as_view(), name='user-logout'),
    path('profile/<slug:slug>', ProfileView.as_view(), name='user-profile'),
]
