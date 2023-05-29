from django.shortcuts import render
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.permissions import AllowAny
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from accounts.serializers import CustomRegisterSerializer, LoginSerializer
from django.conf import settings
from allauth.account.models import EmailAddress, EmailConfirmationHMAC
from dj_rest_auth.registration.serializers import VerifyEmailSerializer
from dj_rest_auth.serializers import JWTSerializer
from dj_rest_auth.utils import jwt_encode
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User, Permission
from django.utils.translation import gettext_lazy as _
from .models import Profile, Address, SMSVerification, DeactivateUser, NationalIDImage
# from .serializers import (
#     ProfileSerializer,
#     UserSerializer,
#     AddressSerializer,
#     CreateAddressSerializer,
#     SMSVerificationSerializer,
#     SMSPinSerializer,
#     DeactivateUserSerializer,
#     PermissionSerializer,
#     PasswordChangeSerializer,
#     UserPermissionSerializer,
#     NationalIDImageSerializer,
# )
# from .send_mail import send_register_mail, send_reset_password_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from allauth.account.utils import send_email_confirmation
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
# from dj_rest_auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView,
from dj_rest_auth.views import LoginView



sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2")
)

class LoginAPIView(LoginView):
# need to fix this overide

    # queryset = ""
    # permission_classes = (AllowAny,)
    # serializer_class = LoginSerializer


    # def get_response(self):
    #     serializer_class = self.get_response_serializer()
    #     if getattr(settings, "REST_USE_JWT", False):
    #         data = {"user": self.user, "token": self.token}
    #         serializer = serializer_class(
    #             instance=data, context={"request": self.request}
    #         )
    #     else:
    #         serializer = serializer_class(
    #             instance=self.token, context={"request": self.request}
    #         )
    #     response = Response(serializer.data, status=status.HTTP_200_OK)

    #     deactivate = DeactivateUser.objects.filter(user=self.user, deactive=True)
    #     if deactivate:
    #         deactivate.update(deactive=False)
    #     return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(
            data=self.request.data, context={"request": request}
        )
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()

@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPIView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = CustomRegisterSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterAPIView, self).dispatch(*args, **kwargs)

    # def get_response_data(self, user):
    #     if getattr(settings, "REST_USE_JWT", False):
    #         data = {"user": user, "token": self.token}
    #     return JWTSerializer(data).data

    def get_response_data(self, user):
        data = {"user": user.pk}

        if getattr(settings, "REST_USE_JWT", False):
            refresh = RefreshToken.for_user(user)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            self.get_response_data(user),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, "REST_USE_JWT", False):
            self.token = jwt_encode(user)

        email = EmailAddress.objects.get(email=user.email, user=user)
        confirmation = EmailConfirmationHMAC(email)
        key = confirmation.key
        # TODO Send mail confirmation here .
        # send_register_mail.delay(user, key)
        print("account-confirm-email/" + key)
        return user


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://www.google.com"
    client_class = OAuth2Client