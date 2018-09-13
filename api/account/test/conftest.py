from typing import Type

import factory

import pytest


class EmailFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating test email instances.
    """
    address = factory.Sequence(lambda n: f'test{n}@example.com')
    user = factory.SubFactory('conftest.UserFactory')

    class Meta:
        model = 'account.Email'


class EmailVerificationFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating test email verifications.
    """
    email = factory.SubFactory('account.test.conftest.EmailFactory')

    class Meta:
        model = 'account.EmailVerification'


@pytest.fixture
def email_factory(db) -> Type[EmailFactory]:
    """
    Fixture to get the factory used to create email addresses.
    """
    return EmailFactory


@pytest.fixture
def email_verification_factory(db) -> Type[EmailVerificationFactory]:
    """
    Fixture to get the factory used to create email verifications.
    """
    return EmailVerificationFactory
