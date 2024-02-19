from django.urls import path

from .views import SignUpView, SignInView, SignOutView, ProfileView

urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/<slug:slug>', ProfileView.as_view(), name='profile'),
]
