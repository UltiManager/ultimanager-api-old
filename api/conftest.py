from typing import Type

import factory

import pytest


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating user instances.
    """
    name = factory.Sequence(lambda n: f'User {n}')

    class Meta:
        model = 'account.User'


@pytest.fixture
def user_factory(db) -> Type[UserFactory]:
    """
    Fixture to get the factory used to create users.
    """
    return UserFactory
