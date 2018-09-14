from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining a token that uses an email address
    instead of the user model's ``USERNAME_FIELD`` attribute.
    """
    username_field = 'email'
