from django.urls import path

from accounts.api.views import (
    TokenObtainPairView,
    TokenRefreshView,
    RegisterAPIView,
    SetPasswordAPIView,
    ChangePasswordAPIView,
    ForgetPasswordAPIView,
)


urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('set-password/', SetPasswordAPIView.as_view(), name='set-password'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('forget-password/', ForgetPasswordAPIView.as_view(), name='forget-password'),

]
