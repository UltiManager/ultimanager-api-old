import os

from django.core.management import BaseCommand, CommandError

from account import models


class Command(BaseCommand):
    """
    Command to create an admin user.
    """
    help = 'Create an admin user'

    def handle(self, *args, **options):
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')

        if not email:
            raise CommandError(
                "The 'ADMIN_EMAIL' environment variable must be set."
            )

        if not password:
            raise CommandError(
                "The 'ADMIN_PASSWORD' environment variable must be set."
            )

        email_query = models.Email.objects.filter(address=email)
        if email_query.exists():
            email_instance = email_query.get()

            if not email_instance.is_verified:
                raise CommandError(
                    f"The email address {email} is already registered but has "
                    "not been verified yet."
                )

            user = email_instance.user

            user.is_staff = True
            user.is_superuser = True
            user.name = 'Admin'

            user.save()
        else:
            admin = models.User.objects.create_superuser('Admin', password)
            models.Email.objects.create(
                address=email,
                is_verified=True,
                user=admin,
            )
