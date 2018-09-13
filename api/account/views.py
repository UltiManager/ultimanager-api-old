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
