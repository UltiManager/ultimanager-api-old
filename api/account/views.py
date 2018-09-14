from rest_framework import generics
from rest_framework.response import Response

from account import serializers


class EmailVerificationView(generics.GenericAPIView):
    """
    post:
    # Verify an Email Address

    Verify an email address using the password of the user who owns the
    email and the token that was emailed to them.
    """
    serializer_class = serializers.EmailVerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class RegistrationView(generics.CreateAPIView):
    """
    post:
    # Register a New User

    Register a new user account. Given a valid email address, name, and
    password, this endpoint will always return a 201 response. This is
    to avoid leaking previously registered email addresses. The user can
    continue the registration flow using the email they receive.
    """
    serializer_class = serializers.RegistrationSerializer
