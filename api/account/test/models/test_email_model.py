from unittest import mock

from django.conf import settings

from account import models


def test_create(db, user_factory):
    """
    Test creating an email address.
    """
    models.Email.objects.create(
        address='test@example.com',
        is_verified=True,
        user=user_factory(),
    )


def test_normalize_address():
    """
    Normalizing the email address should lowercase the domain portion of
    the address as per RFC 5322.
    """
    address = 'MixedCaseLocalPart@funkyDomain.coM'
    expected = 'MixedCaseLocalPart@funkydomain.com'

    assert models.Email.normalize_address(address) == expected


def test_save_normalize(email_factory):
    """
    Email addresses should be normalized on save.
    """
    email = email_factory()
    address = 'MixedCase@funkyDomain.coM'
    email.address = address

    email.save()

    assert email.address == models.Email.normalize_address(address)


def test_send_duplicate_notification(email_factory):
    """
    This method should send a notification to the owner of the email
    that another user attempted to add the email to their account.
    """
    email = email_factory()

    with mock.patch('account.models.email_utils.send_email') as mock_email:
        email.send_duplicate_notification()

    assert mock_email.call_count == 1
    assert mock_email.call_args[1] == {
        'context': {
            'email': email.address,
            'name': email.user.name,
        },
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'recipient_list': [email.address],
        'subject': 'Duplicate Email Registration',
        'template_name': 'account/emails/duplicate-email',
    }


def test_string_conversion(email_factory):
    """
    Converting an email to a string should return a string containing
    the email address and the ID of the object.
    """
    email = email_factory()
    expected = f'{email.address} ({email.id})'

    assert str(email) == expected
