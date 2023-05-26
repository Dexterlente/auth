from django.urls import path, include
from . import views


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
    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path('dj-rest-auth/twitter/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),

    # docs
    # path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    # path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    # path('login/', LoginView.as_view(), name='rest_login'),
    # # URLs that require a user to be logged in with a valid session / token.
    # path('logout/', LogoutView.as_view(), name='rest_logout'),
    # path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    # path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
]
