from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase

from accounts.api.serializers import (
    TokenObtainLifetimeSerializer,
    TokenRefreshLifetimeSerializer,
    UserRegistrationSerializer,
    SetPasswordSerializer,
    ChangePasswordSerializer,
    ForgetPasswordSerializer,
)
from accounts.models import User
from accounts.api.throttles import RegisterThrottle


class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = TokenObtainLifetimeSerializer


class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """
    serializer_class = TokenRefreshLifetimeSerializer


class RegisterAPIView(CreateAPIView):
    """
    post:
        API view that creates a new user and sends verification sms.

    """
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    throttle_classes = (RegisterThrottle,)
    throttle_scope = 'register'


class SetPasswordAPIView(APIView):
    """
    post:
        API view that sets a new password for user.

            body:
                new_password: string
                confirm_password: string
    """
    serializer_class = SetPasswordSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"detail": _("Your password was set successfully.")})


class ChangePasswordAPIView(APIView):
    """
    post:
        API view that changes password for user.

            body:
                old_password: string
                new_password: string
                confirm_password: string
    """
    serializer_class = ChangePasswordSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"detail": _("Your password was set successfully.")})


class ForgetPasswordAPIView(APIView):
    """
    post:
        API view for requesting new verification code for users that has forgotten their passwords.

            body:
                phone_number: string
    """
    serializer_class = ForgetPasswordSerializer
    throttle_classes = (RegisterThrottle,)
    throttle_scope = 'register'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": _("Verification code has been successfully sent.")})
