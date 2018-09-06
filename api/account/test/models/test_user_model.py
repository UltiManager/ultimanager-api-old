from account import models


def test_create_user(db):
    """
    Test creating a user instance.
    """
    models.User.objects.create(
        is_active=True,
        is_staff=False,
        is_superuser=False,
        name='John Doe',
    )


def test_string_conversion(user_factory):
    """
    Converting a user to a string should return the user's name.
    """
    user = user_factory()

    assert str(user) == user.name
