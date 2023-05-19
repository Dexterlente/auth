from django.urls import path, include
from . import views


# igot sick im sorry
# 13 05 still sick
# 14 damn it still sick
# 15 im tired
# 16 maybe last
# 17 im ok but still
# 19 maybe last
urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login')
]
