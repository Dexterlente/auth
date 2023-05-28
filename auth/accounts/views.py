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
from accounts.serializers import CustomRegisterSerializer
from django.conf import settings
from allauth.account.models import EmailAddress, EmailConfirmationHMAC

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("password1", "password2")
)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPIView(RegisterView):
    permission_classes = [AllowAny]
    serializer_class = CustomRegisterSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(RegisterAPIView, self).dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if getattr(settings, "REST_USE_JWT", False):
            data = {"user": user, "token": self.token}
        return JWTSerializer(data).data

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

    
# class FacebookAuthView(APIView):
#     def post(self, request):
#         access_token = request.POST.get('access_token')
#         if access_token:
#             # Perform registration or login logic here using the access_token
#             # Return appropriate response indicating success or failure
#             return Response({'message': 'Registration or login successful'})
#         else:
#             return Response({'message': 'Access token is required'}, status=400)

class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://www.google.com"
    client_class = OAuth2Client