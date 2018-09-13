from rest_framework import status
from rest_framework.reverse import reverse

from account import serializers

PASSWORD = 'password'


def test_post_invalid_token(api_client, db):
    """
    Sending a POST request with an invalid token should return a 400
    response.
    """
    data = {
        'password': PASSWORD,
        'token': 'made-up-token',
    }

    url = reverse('account:email-verification')
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    serializer = serializers.EmailVerificationSerializer(data=data)
    assert not serializer.is_valid()

    assert response.data == serializer.errors


def test_post_valid_token(
        api_client,
        email_verification_factory,
        user_factory):
    """
    Sending a POST request to the endpoint with valid credentials should
    verify the user's email address.
    """
    user = user_factory(password=PASSWORD)
    verification = email_verification_factory(email__user=user)
    email = verification.email

    data = {
        'password': PASSWORD,
        'token': verification.token,
    }

    url = reverse('account:email-verification')
    response = api_client.post(url, data)

    email.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {}
    assert email.is_verified
