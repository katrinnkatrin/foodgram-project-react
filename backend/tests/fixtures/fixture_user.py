import pytest
from rest_framework.test import APIClient


@pytest.fixture
def user_client(django_user_model):
    user = django_user_model.objects.create_user(
        email='user@yandex.ru',
        username='user',
        first_name='user',
        last_name='user',
        password='Qwerty123!'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser', password='1234567')


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser2', password='1234567')


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUserAnother', password='1234567')
