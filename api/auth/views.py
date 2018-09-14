from rest_framework_simplejwt.views import TokenObtainPairView

from auth import serializers


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain a token pair that uses our email based
    serializer.
    """
    serializer_class = serializers.EmailTokenObtainPairSerializer
