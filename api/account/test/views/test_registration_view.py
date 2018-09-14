from account import serializers, views


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.RegistrationView()

    assert view.get_serializer_class() == serializers.RegistrationSerializer
