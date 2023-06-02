# auth
#### authentication app
###### base of dj-rest-auth
Application for account management  
Account registration  
For login with social accounts and phonenumbers login with email and phone confirmation  
an api build with serializers for your frontend of your choice  

##### Endpoints

    # csrftoken
    'get-csrf-token/'
    # custom login
    login/
    # custom registration
    dj-rest-auth/registration/
        # verify
    dj-rest-auth/registration/verify-email/
    dj-rest-auth/registration/resend-email/
    # social accounts login
    'dj-rest-auth/facebook/'
    'dj-rest-auth/twitter/'
    'dj-rest-auth/google/'
    # dj-rest-auth logout
    'logout/'
    # reset pass

    password/reset/
    authentication/password/reset/confirm/'
#####  phone verification endpoint
    verify-sms/<int:pk>/"
    resend-sms/"
    Twilio api is used for phone verification
###### auth users
    'user/'
    password/change/'