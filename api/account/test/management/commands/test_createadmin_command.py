import pytest
from django.core import management

from account import models

EMAIL = 'admin@exmaple.com'
PASSWORD = 'password'


@pytest.fixture
def admin_env(env):
    """
    Fixture to get an environment with admin credentials.
    """
    env['ADMIN_EMAIL'] = EMAIL
    env['ADMIN_PASSWORD'] = PASSWORD

    return env


def test_create_admin_email_exists_unverified(admin_env, email_factory):
    """
    If the admin email already exists in the system but is unverified,
    the command should fail.
    """
    email_factory(address=EMAIL, is_verified=False)

    with pytest.raises(management.CommandError):
        management.call_command('createadmin')

    # No new user or email should be created
    assert models.Email.objects.count() == 1
    assert models.User.objects.count() == 1


def test_create_admin_email_exists_verified(
        admin_env,
        email_factory,
        user_factory):
    """
    If the admin email exists in the system and is verified, the user
    attached to the email should be promoted to an admin.
    """
    user = user_factory(is_staff=False, is_superuser=False, name='Not Admin')
    email_factory(address=EMAIL, is_verified=True, user=user)

    management.call_command('createadmin')
    user.refresh_from_db()

    assert user.is_staff
    assert user.is_superuser
    assert user.name == 'Admin'


def test_create_admin_new(admin_env, db):
    """
    If the email specified doesn't exist, it should be created along
    with a new admin user.
    """
    management.call_command('createadmin')

    user = models.User.objects.get()
    email = models.Email.objects.get()

    assert user.name == 'Admin'
    assert user.is_staff
    assert user.is_superuser
    assert user.check_password(PASSWORD)

    assert email.address == EMAIL
    assert email.is_verified


def test_create_admin_no_email(admin_env, db):
    """
    If no email is specified, a ``CommandError`` should be raised.
    """
    del admin_env['ADMIN_EMAIL']

    with pytest.raises(management.CommandError):
        management.call_command('createadmin')


def test_create_admin_no_password(admin_env, db):
    """
    If no password is specified, a ``CommandError`` should be raised.
    """
    del admin_env['ADMIN_PASSWORD']

    with pytest.raises(management.CommandError):
        management.call_command('createadmin')
