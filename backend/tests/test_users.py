import pytest

from django.contrib.auth import get_user_model

User = get_user_model()


class TestUsersAPI:
    url_create = '/api/users/'
    ch_pass = '/api/users/set_password/'
    token_login = '/api/auth/token/login/'
    token_logout = '/api/auth/token/logout/'

    @pytest.mark.django_db(transaction=True)
    def test_users_not_authenticated(self, client):
        response = client.get(self.url_create)

        code = 200
        assert response.status_code == code, (
            f'Анонимный пользователь при get запросе {self.url_create}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_authenticated(self, user_client):
        response = user_client.get(self.url_create)

        code = 200
        assert response.status_code == code, (
            f'Авторизованный пользователь при get запросе {self.url_create}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_users_valid_data(self, client):
        valid_data = {
            'email': 'vasya@yandex.ru',
            'username': 'vasya',
            'first_name': 'Вася',
            'last_name': 'Пупкин',
            'password': 'Qwerty123!'
        }
        response = client.post(self.url_create, data=valid_data)

        code = 201
        assert response.status_code == code, (
            f'При запросе с валидными данными на {self.url_create}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_users_not_valid_data(self, client):
        not_valid_data = {
            'email': '11111111111',
            'username': '111111',
            'first_name': '111111',
            'last_name': '1111111',
            'password': 'Qwerty123!'
        }
        response = client.post(self.url_create, data=not_valid_data)

        code = 400
        assert response.status_code == code, (
            f'При запросе с не валидными данными на {self.url_create}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_users_invalid_data(self, client):
        response = client.post(self.url_create, data=None)

        code = 400
        assert response.status_code == code, (
            f'При запросе без данных на {self.url_create}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_profile_user_not_authenticated(self, client, user):
        response = client.get(f'{self.url_create}1/')
        code = 401
        assert response.status_code == code, (
            f'При запросе на {self.url_create}1/'
            '- не авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_profile_user_authenticated(self, user_client, user_2):
        response = user_client.get(f'{self.url_create}{user_2.id}/')

        code = 200
        assert response.status_code == code, (
            f'При запросе на {self.url_create}{user_2.id}/'
            '- авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_me_not_authenticated(self, client):
        response = client.get(f'{self.url_create}me/')

        code = 401
        assert response.status_code == code, (
            f'При запросе на {self.url_create}me/'
            '- не авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_me_authenticated(self, user_client):
        response = user_client.get(f'{self.url_create}me/')

        code = 200
        assert response.status_code == code, (
            f'При запросе на {self.url_create}me/'
            '- авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.skip(reason="Не валидные данные")
    @pytest.mark.django_db(transaction=True)
    def test_user_set_password_valid(self, user_client):
        valid_data = {
            'new_password': 'string',
            'current_password': 'Qwerty123!'
        }
        response = user_client.post(f'{self.ch_pass}', data=valid_data)

        code = 204
        assert response.status_code == code, (
            f'При запросе на {self.ch_pass} с валидными данными'
            '- авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_set_password_not_valid(self, user_client):
        valid_data = {
            'new_password': 'string'
        }
        response = user_client.post(f'{self.ch_pass}', data=valid_data)

        code = 400
        assert response.status_code == code, (
            f'При запросе на {self.ch_pass} с не валидными данными'
            '- авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_client_set_password_valid(self, client):
        valid_data = {
            'new_password': 'string',
            'current_password': 'Qwerty123!'
        }
        response = client.post(f'{self.ch_pass}', data=valid_data)

        code = 401
        assert response.status_code == code, (
            f'При запросе на {self.ch_pass} с валидными данными'
            '- не авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.skip(reason="Не валидные данные")
    @pytest.mark.django_db(transaction=True)
    def test_user_token_login(self, user_client):
        valid_data = {
            'password': 'Qwerty123!',
            'email': 'user@yandex.ru'
        }
        response = user_client.post(f'{self.ch_pass}', data=valid_data)

        code = 201
        assert response.status_code == code, (
            f'При запросе на {self.token_login} с почтой и паролем'
            '- авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_token_logout(self, user_client):
        response = user_client.post(f'{self.token_logout}')

        code = 204
        assert response.status_code == code, (
            f'При запросе на {self.token_logout}'
            '- авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_token_logout_client(self, client):
        response = client.post(f'{self.token_logout}')

        code = 401
        assert response.status_code == code, (
            f'При запросе на {self.token_logout}'
            '- не авторизованный пользователь'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_get(self, user_client, user_2):
        response = user_client.get(f'{self.url_create}')

        test_data = response.json()
        assert type(test_data) == dict, (
            f'При GET запросе на {self.url_create} должен вернуться словарь'
        )

        assert len(test_data['results']) == User.objects.all().count(), (
            'При GET запросе должен возвращаться весь список'
        )

        test_user = test_data['results'][0]
        assert 'id' in test_user, (
            'Проверить, что `id` в списке полей `fields`, '
            'сериализатора модели User'
        )

        assert 'username' in test_user, (
            'Проверить, что `username` в списке полей `fields`, '
            'сериализатора модели User'
        )

        assert 'email' in test_user, (
            'Проверить, что `email` в списке полей `fields`, '
            'сериализатора модели User'
        )

        assert 'first_name' in test_user, (
            'Проверить, что `first_name` в списке полей `fields`, '
            'сериализатора модели User'
        )

        assert 'last_name' in test_user, (
            'Проверить, что `last_name` в списке полей `fields`, '
            'сериализатора модели User'
        )

        assert 'is_subscribed' in test_user, (
            'Проверить, что `is_subscribed` в списке полей `fields`, '
            'сериализатора модели User'
        )
