from django.utils.translation import ugettext as _
from rest_framework import serializers

from account import models


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for verifying an email address.
    """
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._verification: models.EmailVerification = None

    def save(self):
        """
        Verify the email address associated with the provided
        verification token.
        """
        self._verification.verify()

    def validate(self, data):
        """
        Validate the provided token and password.

        At this point we have the verification object cached, so we use
        it to look up the associated ``Email`` and ``User`` instances.
        If the provided password does not match the user, a
        ``serializers.ValidationError`` is raised.

        Args:
            data:
                The data received by the serializer.

        Returns:
            The validated data.
        """
        if not self._verification.email.user.check_password(data['password']):
            raise serializers.ValidationError(
                code='invalid_password',
                detail={
                    'password': (
                        _('The provided password does not match the owner of '
                          'the email.'),
                    ),
                },
            )

        return data

    def validate_token(self, token):
        """
        Validate the received token to make sure it exists and has not
        expired.

        Args:
            token:
                The token received by the serializer.

        Returns:
            The validated token.

        Raises:
            serializers.ValidationError:
                If the provided token does not exist or has expired.
        """
        try:
            self._verification = models.EmailVerification.objects.get(
                token=token,
            )
        except models.EmailVerification.DoesNotExist:
            raise serializers.ValidationError(
                code='invalid_token',
                detail=_('The provided token does not exist or has expired.'),
            )

        return token
