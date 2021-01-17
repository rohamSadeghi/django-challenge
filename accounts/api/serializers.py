from random import randint

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken


from accounts.models import User


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=120)
    has_password = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'has_password')
        extra_kwargs = {'phone_number': {'validators': None}}

    def get_has_password(self, obj):
        return obj.has_usable_password()


    def create(self, validated_data):
        if not settings.DEVEL:
            verify_code = randint(10000, 99999)
        else:
            verify_code = 11111

        # TODO: Should add some regex validation for checking that phone number is valid
        phone_number = int(validated_data['phone_number'])

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create_user(
                phone_number=phone_number
            )

        if user.has_usable_password():
            return user
        user.set_verify_code(verify_code)
        return user


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    'new_password':
                        _('New password and confirm password are not matched.')
                }
            )
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        if user.has_usable_password():
            raise serializers.ValidationError(_("This user has already set password before"))
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    'new_password':
                        _('New password and confirm password are not matched.')
                }
            )
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        if not user.check_password(validated_data['old_password']):
            raise PermissionDenied()
        user.set_password(validated_data['new_password'])
        user.save()
        return user


class ForgetPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=120)

    def validate(self, attrs):
        # TODO: Should add some regex validation for checking that phone number is valid
        raw_phone_number = attrs.get('phone_number')

        if not settings.DEVEL:
            verify_code = randint(10000, 99999)
        else:
            verify_code = 11111

        try:
            user = User.objects.get(phone_number=raw_phone_number)
        except User.DoesNotExist:
            raise NotFound()
        cache.set(f'forget_password_{user.phone_number}_{verify_code}', True, 6.5 * 60 * 60)
        user.set_verify_code(verify_code)
        data = super().validate(attrs)
        return data
