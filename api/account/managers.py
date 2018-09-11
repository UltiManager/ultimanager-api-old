from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Manager for our custom User objects.
    """

    def create_superuser(self, name: str, password: str, **kwargs):
        """
        Create a user who is implicitly granted all permissions.

        Args:
            name:
                The user's name.
            password:
                The user's password.
            **kwargs:
                Additional arguments to pass to the User instance being
                created.

        Returns:
            A new user instance with the provided attributes. Notably,
            ``is_staff`` and ``is_superuser`` will be set to ``True``.
        """
        user = self.model(name=name, **kwargs)
        user.set_password(password)

        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user

    def create_user(self, name: str, password: str, **kwargs):
        """
        Create a new user.

        Args:
            name:
                The user's name.
            password:
                The user's password.
            **kwargs:
                Additional arguments to pass to the User instance being
                created.

        Returns:
            A new user instance with the provided attributes.
        """
        user = self.model(name=name, **kwargs)
        user.set_password(password)
        user.save()

        return user
