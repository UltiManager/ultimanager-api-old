from typing import Type

import factory

import pytest


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for generating user instances.
    """
    name = factory.Sequence(lambda n: f'User {n}')
    password = 'password'

    class Meta:
        model = 'account.User'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Create a new user.

        Args:
            model_class:
                The class to instantiate.
            *args:
                Positional arguments to pass to the model.
            **kwargs:
                Keyword arguments to pass to the model.

        Returns:
            The newly created user instance.
        """
        manager = cls._get_manager(model_class)

        return manager.create_user(*args, **kwargs)


@pytest.fixture
def user_factory(db) -> Type[UserFactory]:
    """
    Fixture to get the factory used to create users.
    """
    return UserFactory
