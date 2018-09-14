from unittest import mock

from django.conf import settings

from account import models


def test_create(email_factory):
    """
    Test creating an email verification.
    """
    models.EmailVerification.objects.create(
        email=email_factory(),
    )


def test_repr(email_verification_factory):
    """
    Test the repr of the instance.
    """
    verification = email_verification_factory()
    expected = (f'EmailVerification(id={verification.id}, '
                f'email_address="{verification.email.address}")')

    assert repr(verification) == expected


def test_send_email(email_verification_factory):
    """
    This method should send a verification email to the associated email
    address.
    """
    verification = email_verification_factory()

    with mock.patch('account.models.email_utils.send_email') as mock_email:
        verification.send_email()

    assert mock_email.call_count == 1
    assert mock_email.call_args[1] == {
        'context': {
            'name': verification.email.user.name,
            'token': verification.token,
        },
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': [verification.email.address],
        'subject': 'Please Verify Your Email',
        'template_name': 'account/emails/verify-email',
    }


def test_string_conversion(email_verification_factory):
    """
    Converting an email verification to a string should return a string
    indicating which email address the verification is associated with.
    """
    verification = email_verification_factory()
    expected = f'Email Verification for {verification.email.address}'

    assert str(verification) == expected


def test_verify(email_factory, email_verification_factory):
    """
    The verify method should mark the associated email as verified and
    delete the verification instance.
    """
    email = email_factory(is_verified=False)
    verification = email_verification_factory(email=email)

    verification.verify()
    email.refresh_from_db()

    assert email.is_verified
    assert models.EmailVerification.objects.count() == 0
