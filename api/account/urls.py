from django.urls import path

from account import views


app_name = 'account'


urlpatterns = [
    path(
        'email-verification/',
        views.EmailVerificationView.as_view(),
        name='email-verification',
    ),

    path(
        'users/',
        views.RegistrationView.as_view(),
        name='registration',
    ),
]
