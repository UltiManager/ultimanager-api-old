"""
Integration tests for the process of registering a new user.
"""

import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from account import models


@pytest.mark.integration
def test_register_user(api_client, db):
    """
    Test registering a new user.
    """
    data = {
        'email': 'test@example.com',
        'name': 'John Smith',
        'password': 'MySuperSecretPassword',
    }

    url = reverse('account:registration')
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == {
        'email': data['email'],
        'name': data['name'],
    }

    assert models.User.objects.count() == 1
    assert models.Email.objects.count() == 1
    assert models.EmailVerification.objects.count() == 1
