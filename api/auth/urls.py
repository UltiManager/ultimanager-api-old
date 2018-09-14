from django.urls import path
from rest_framework_simplejwt.views import token_refresh

from auth import views


app_name = 'auth'


urlpatterns = [
    path(
        'token/',
        views.EmailTokenObtainPairView.as_view(),
        name='token-obtain',
    ),
    path(
        'token/refresh/',
        token_refresh,
        name='token-refresh',
    ),
]
