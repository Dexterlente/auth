from django.urls import path, include, re_path
from . import views
from dj_rest_auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, UserDetailsView, PasswordChangeView


# igot sick im sorry
# 13 05 still sick
# 14 damn it still sick
# 15 im tired
# 16 maybe last
# 17 im ok but still
# 19 maybe last
# 21
# D
# 22
# 26
urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="account_login"),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path("dj-rest-auth/registration/", views.RegisterAPIView.as_view(), name="account_signup"),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    # path('fb-register/', views.FacebookAuthView.as_view(), name='fb_auth'),
    path('dj-rest-auth/twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    # dj-rest-auth logout
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    # reset pass
    re_path(r'^dj-rest-auth/password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    # re_path(r'^password/reset/$', views.ThePasswordResetView.as_view(), name='password_reset'),
    re_path(r'^authentication/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
     PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

# auth users
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
]
