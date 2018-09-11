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


def test_manager_create_superuser(db):
    """
    Creating a superuser should be identical to creating a normal user
    except ``is_staff`` and ``is_superuser`` should be set to ``True``.
    """
    name = 'John Doe'
    password = 'password'

    user = models.User.objects.create_superuser(
        name=name,
        password=password,
    )

    assert user.is_staff
    assert user.is_superuser
    assert user.name == name
    assert user.check_password(password)


def test_manager_create_user(db):
    """
    Test creating a user through the model's manager.
    """
    name = 'John Doe'
    password = 'password'

    user = models.User.objects.create_user(
        name=name,
        password=password,
    )

    assert user.name == name
    assert user.check_password(password)


def test_string_conversion(user_factory):
    """
    Converting a user to a string should return the user's name.
    """
    user = user_factory()

    assert str(user) == user.name
