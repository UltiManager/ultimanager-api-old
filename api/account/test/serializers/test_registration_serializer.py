from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from rest_framework import serializers as drf_serializers

from account import serializers, models

EMAIL = 'test@example.com'
NAME = 'John Smith'
PASSWORD = 'C0rrectH0rseBatteryStaple'


@mock.patch(
    'account.serializers.models.Email.send_duplicate_notification',
    autospec=True,
)
def test_save_duplicate_email(_, email_factory):
    """
    If the provided email already exists and is verified, that email
    should have a duplicate registration notification sent to it.
    """
    email = email_factory(is_verified=True)
    data = {
        'email': email.address,
        'name': NAME,
        'password': PASSWORD,
    }
    serializer = serializers.RegistrationSerializer(data=data)

    assert serializer.is_valid()
    serializer.save()

    # The only user should be the owner of the email; no new user
    assert models.User.objects.get() == email.user
    # No new email address should have been created
    assert models.Email.objects.get() == email
    # A duplicate notification should have been sent
    assert email.send_duplicate_notification.call_count == 1


@mock.patch(
    'account.serializers.models.EmailVerification.send_email',
    autospec=True,
)
def test_save_duplicate_email_unverified(_, email_factory):
    """
    If the provided email exists but is not verified, another
    verification email should be sent to the address.
    """
    email = email_factory(is_verified=False)
    data = {
        'email': email.address,
        'name': NAME,
        'password': PASSWORD,
    }
    serializer = serializers.RegistrationSerializer(data=data)

    assert serializer.is_valid()
    serializer.save()

    # No new user should be created.
    assert models.User.objects.get() == email.user
    # No new email should be created
    assert models.Email.objects.get() == email
    # There should be a new email verification sent
    verification = email.verifications.get()
    assert verification.send_email.call_count == 1


@mock.patch(
    'account.serializers.models.EmailVerification.send_email',
    autospec=True,
)
def test_save_valid_data(_, db):
    """
    If valid data is provided, a new user and email should be created.
    """
    data = {
        'email': EMAIL,
        'name': NAME,
        'password': PASSWORD,
    }
    serializer = serializers.RegistrationSerializer(data=data)

    assert serializer.is_valid()
    serializer.save()

    user = models.User.objects.get()
    email = models.Email.objects.get()

    assert user.name == NAME
    assert user.check_password(PASSWORD)
    assert user.primary_email == email

    assert email.address == EMAIL
    assert not email.is_verified
    assert email.user == user

    verification = email.verifications.get()
    assert verification.send_email.call_count == 1

    assert serializer.data == {
        'email': EMAIL,
        'name': NAME,
    }


def test_validate_email():
    """
    Validating the email address should return its normalized version.
    """
    serializer = serializers.RegistrationSerializer()
    email = 'FunkyEmail@Example.Com'
    expected = models.Email.normalize_address(email)

    assert serializer.validate_email(email) == expected


def test_validate_password_invalid():
    """
    If the provided password fails password validation, the returned
    error should be re-raised as DRF's ``ValidationError``.
    """
    exception = ValidationError(['error', 'list'], code='invalid_password')
    serializer = serializers.RegistrationSerializer()

    with mock.patch(
            'account.serializers.password_validation.validate_password',
            autospec=True,
            side_effect=exception):
        with pytest.raises(drf_serializers.ValidationError) as ex_info:
            serializer.validate_password(PASSWORD)

    assert ex_info.value.detail == exception.error_list


def test_validate_password_valid():
    """
    If the provided password passes Django's password validation, it
    should be returned as is.
    """
    serializer = serializers.RegistrationSerializer()

    with mock.patch(
        'account.serializers.password_validation.validate_password',
        autospec=True,
    ) as mock_validate:
        result = serializer.validate_password(PASSWORD)

    assert result == PASSWORD
    assert mock_validate.call_count == 1
    assert mock_validate.call_args[0] == (PASSWORD,)
