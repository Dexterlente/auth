from django.urls import path, include
from . import views


urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login')
    path('dj-rest-auth/twitter/', views.TwitterLogin.as_view(), name='twitter_login')
]
