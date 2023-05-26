from django.shortcuts import render
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.response import Response
from rest_framework.views import APIView

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