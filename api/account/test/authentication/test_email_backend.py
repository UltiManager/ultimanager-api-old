import pytest

from account import authentication

PASSWORD = 'password'


@pytest.fixture
def auth_backend() -> authentication.EmailBackend:
    """
    Fixture to get an instance of the authentication backend.
    """
    return authentication.EmailBackend()


def test_authenticate_inactive_user(
        auth_backend,
        email_factory,
        user_factory):
    """
    If the provided credentials belong to an inactive user, the ``None``
    should be returned.
    """
    user = user_factory(is_active=False, password=PASSWORD)
    email = email_factory(is_verified=True, user=user)

    result = auth_backend.authenticate(
        None,
        email=email.address,
        password=PASSWORD,
    )

    assert result is None


def test_authenticate_missing_email(auth_backend, db):
    """
    If the provided email address does not exist in the system, ``None``
    should be returned.
    """
    result = auth_backend.authenticate(
        None,
        email='non-existent@example.com',
        password=PASSWORD,
    )

    assert result is None


def test_authenticate_unverified_email(
        auth_backend,
        email_factory,
        user_factory):
    """
    If the provided email address exists in the system but has not been
    verified, authentication should return ``None``.
    """
    user = user_factory(password=PASSWORD)
    email = email_factory(is_verified=False, user=user)

    result = auth_backend.authenticate(
        None,
        email=email.address,
        password=PASSWORD,
    )

    assert result is None


def test_authenticate_valid_credentials(
        auth_backend,
        email_factory,
        user_factory):
    """
    If provided valid credentials, the backend should return the
    corresponding user.
    """
    user = user_factory(password=PASSWORD)
    email = email_factory(is_verified=True, user=user)

    result = auth_backend.authenticate(
        None,
        email=email.address,
        password=PASSWORD,
    )

    assert result == user


def test_authenticate_valid_credentials_alias(
        auth_backend,
        email_factory,
        user_factory):
    """
    The ``username`` parameter should be an alias for the ``email``
    parameter.
    """
    user = user_factory(password=PASSWORD)
    email = email_factory(is_verified=True, user=user)

    result = auth_backend.authenticate(
        None,
        password=PASSWORD,
        username=email.address,
    )

    assert result == user


def test_authenticate_wrong_password(
        auth_backend,
        email_factory,
        user_factory):
    """
    If the wrong password is provided, ``None`` should be returned.
    """
    user = user_factory(password=PASSWORD)
    email = email_factory(is_verified=True, user=user)

    result = auth_backend.authenticate(
        None,
        email=email.address,
        password=PASSWORD * 2,
    )

    assert result is None


def test_get_user(auth_backend, user_factory):
    """
    The user with the given ID should be returned if they exist.
    """
    user = user_factory()

    assert auth_backend.get_user(user.id) == user


def test_get_user_invalid_id(auth_backend, db):
    """
    If there is no user with the given ID, ``None`` should be returned.
    """
    assert auth_backend.get_user(None) is None
