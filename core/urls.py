from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import OTPRequestView, OTPVerificationView, SetPasswordView, LoginView, ProfileView


urlpatterns = [
    path('send/', OTPRequestView.as_view(), name='auth-start'),
    path('verify/', OTPVerificationView.as_view(), name='auth-verify'),
    path('set-password/', SetPasswordView.as_view(), name='set-password'),
    path('login/', LoginView.as_view(), name='login'),
]

router = DefaultRouter()
router.register(r"profile", ProfileView, basename='profile')


urlpatterns += router.urls
