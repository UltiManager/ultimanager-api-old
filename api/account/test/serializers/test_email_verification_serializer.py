from unittest import mock

import pytest
from rest_framework import serializers as drf_serializers

from account import serializers


PASSWORD = 'password'


def test_save_valid(email_verification_factory, user_factory):
    """
    Given a valid token and password combination, saving the serializer
    should verify the email.
    """
    user = user_factory(password=PASSWORD)
    verification = email_verification_factory(email__user=user)

    data = {
        'password': PASSWORD,
        'token': verification.token,
    }

    serializer = serializers.EmailVerificationSerializer(data=data)
    assert serializer.is_valid()

    with mock.patch(
        'account.serializers.models.EmailVerification.verify',
        autospec=True,
    ) as mock_verify:
        serializer.save()

    assert mock_verify.call_count == 1


def test_validate_invalid_password(email_verification_factory, user_factory):
    """
    If the provided password does not match the user who created the
    verification, the serializer should fail to validate.
    """
    user = user_factory(password=PASSWORD)
    verification = email_verification_factory(email__user=user)

    data = {
        'password': PASSWORD * 2,
        'token': verification.token,
    }
    serializer = serializers.EmailVerificationSerializer(data=data)

    with pytest.raises(drf_serializers.ValidationError) as ex_info:
        serializer.is_valid(raise_exception=True)

    assert ex_info.value.detail['password'][0].code == 'invalid_password'


def test_validate_invalid_token(db):
    """
    If the provided token does not exist, the serializer should fail to
    validate.
    """
    data = {
        'password': PASSWORD,
        'token': 'made-up-token',
    }
    serializer = serializers.EmailVerificationSerializer(data=data)

    with pytest.raises(drf_serializers.ValidationError) as ex_info:
        serializer.is_valid(raise_exception=True)

    assert ex_info.value.detail['token'][0].code == 'invalid_token'
