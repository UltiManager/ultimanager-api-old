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


def test_string_conversion(email_factory):
    """
    Converting an email to a string should return a string containing
    the email address and the ID of the object.
    """
    email = email_factory()
    expected = f'{email.address} ({email.id})'

    assert str(email) == expected
