from django.urls import path

from .views import SignUpView, SignInView, SignOutView, ProfileView

urlpatterns = [
    path('user/register/', SignUpView.as_view(), name='user-register'),
    path('user/login/', SignInView.as_view(), name='user-login'),
    path('user/logout/', SignOutView.as_view(), name='user-logout'),
    path('user/profile/<slug:slug>', ProfileView.as_view(), name='user-profile'),
]
