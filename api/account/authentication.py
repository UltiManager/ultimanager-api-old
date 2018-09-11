from django.contrib.auth import get_user_model

from account import models


UserModel = get_user_model()


class EmailBackend:
    """
    Authentication backend that allows users to login with any verified
    email address that they own.
    """

    @staticmethod
    def authenticate(_, email=None, username=None, password=None):
        """
        Authenticate a user.

        Args:
            _:
                The request made to authenticate the user. This
                parameter is required by Django, but unused here.
            email:
                The user's email address.
            username:
                An alias for the ``email`` parameter. This is used to
                maintain compatibility with Django's default
                authentication forms.
            password:
                The user's password.

        Returns:
            The user corresponding to the provided credentials. If no
            users match, ``None`` is returned.

        Raises:
            PermissionDenied:
                If the account of the user corresponding to the provided
                credentials is not active.
        """
        email = email or username

        try:
            email_instance = models.Email.objects.get(
                address=email,
                is_verified=True,
            )
        except models.Email.DoesNotExist:
            return None

        user = email_instance.user

        if not all((user.check_password(password), user.is_active)):
            return None

        return user

    @staticmethod
    def get_user(user_id):
        """
        Get a user by their ID.

        Args:
            user_id:
                The ID of the user to fetch.

        Returns:
            The user with the provided ID. ``None`` is returned if no
            user with the provided ID exists.
        """
        try:
            return UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None
