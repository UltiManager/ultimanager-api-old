import logging

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _, ugettext_lazy
from rest_framework import serializers

from account import models


logger = logging.getLogger(__name__)


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for verifying an email address.
    """
    password = serializers.CharField(
        help_text=ugettext_lazy(
            "The password of the user who added the email address to their "
            "account."
        ),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(
        help_text=ugettext_lazy(
            "The token that was emailed to the address being verified."
        ),
        write_only=True,
    )

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


class RegistrationSerializer(serializers.Serializer):
    """
    Serializer for registering new users.
    """
    email = serializers.EmailField(
        help_text=ugettext_lazy(
            "The user's email address."
        ),
    )
    name = serializers.CharField(
        help_text=ugettext_lazy(
            "The public facing name the user wishes to be identified as. This "
            "value does not have to be unique."
        ),
    )
    password = serializers.CharField(
        help_text=ugettext_lazy("The user's password."),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True,
    )

    def save(self):
        """
        Register a new user with the provided information.

        If the email already exists and is verified, a notification is
        sent to the email address. If the email exists but is not
        verified, a new verification email is sent. If the email does
        not exist, a new user and email are created, and a verification
        email is sent to the new email.
        """
        email = self.validated_data['email']
        name = self.validated_data['name']
        password = self.validated_data['password']

        email_query = models.Email.objects.filter(address=email)
        if email_query.exists():
            email_instance = email_query.get()

            # If the email is already verified, we send a duplicate
            # notification and exit.
            if email_instance.is_verified:
                logger.info(
                    "Not registering a new user because the email address %r "
                    "is already verified.",
                    email_instance,
                )
                email_instance.send_duplicate_notification()

                return

            # If the email is not verified, we send a new verification
            # token to the address.
            logger.info(
                "Not registering a new user because the email address %r "
                "already exists. Sending a new verification token instead."
            )
            verification = models.EmailVerification.objects.create(
                email=email_instance,
            )
            verification.send_email()

            return

        # The email doesn't exist, so we create a new user and email,
        # then send a verification token to the email.
        user = models.User.objects.create_user(name, password)
        email_instance = models.Email.objects.create(address=email, user=user)

        # The user's primary email is their only email. This is the only
        # time the primary email can be unverified.
        user.primary_email = email_instance
        user.save()

        logger.info(
            "Registered new user %r with email address %r",
            user,
            email_instance,
        )

        verification = models.EmailVerification.objects.create(
            email=email_instance,
        )
        verification.send_email()

    def validate_email(self, email):
        """
        Normalize the provided email address.

        Args:
            email:
                The email address provided to the serializer.

        Returns:
            The normalized version of the provided email.
        """
        return models.Email.normalize_address(email)

    def validate_password(self, password):
        """
        Pass the provided password through Django's password validation.

        Args:
            password:
                The password provided to the serializer.

        Returns:
            The validated password.
        """
        # Re-raise the validation error from Django as DRF's
        # ``ValidationError`` so that the middleware can correctly
        # catch it and render a response.
        try:
            password_validation.validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(
                code='invalid_password',
                detail=e.error_list,
            )

        return password
