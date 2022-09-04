import pytest

from recipes.models import Tag


class TestTagAPI:
    tags = '/api/tags/'

    @pytest.mark.django_db(transaction=True)
    def test_tag_not_authenticated(self, client):
        response = client.get(f'{self.tags}')

        code = 200
        assert response.status_code == code, (
            f'Анонимный пользователь при get запросе {self.tags} '
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_tag_authenticated(self, user_client):
        response = user_client.get(f'{self.tags}')

        code = 200
        assert response.status_code == code, (
            f'Авторизиванный пользователь при get запросе {self.tags} '
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_tag_id_not_authenticated(self, client, tag_1):
        response = client.get(f'{self.tags}{tag_1.id}/')

        code = 200
        assert response.status_code == code, (
            f'Анонимный пользователь при get запросе {self.tags}{tag_1.id}/'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_tag_id_authenticated(self, user_client, tag_1):
        response = user_client.get(f'{self.tags}{tag_1.id}/')

        code = 200
        assert response.status_code == code, (
            'Авторизованный пользователь при get запросе'
            f'- на {self.tags}{tag_1.id}/'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_tag_id_not_valid(self, client):
        response = client.get(f'{self.tags}4/')

        code = 404
        assert response.status_code == code, (
            f'Анонимный пользователь при get запросе {self.tags}4/ , '
            'на не существующий id'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_tag_get(self, user_client, tag_1, tag_2):
        response = user_client.get(f'{self.tags}')

        test_data = response.json()
        assert type(test_data) == dict, (
            f'При GET запросе на {self.tags} должен вернуться словарь'
        )

        assert len(test_data['results']) == Tag.objects.all().count(), (
            'При GET запросе должен возвращаться весь список'
        )

        test_tag = test_data['results'][0]
        assert 'id' in test_tag, (
            'Проверить, что `id` в списке полей `fields`, '
            'сериализатора модели Tag'
        )

        assert 'name' in test_tag, (
            'Проверить, что `name` в списке полей `fields`, '
            'сериализатора модели Tag'
        )

        assert 'color' in test_tag, (
            'Проверить, что `color` в списке полей `fields`, '
            'сериализатора модели Tag'
        )

        assert 'slug' in test_tag, (
            'Проверить, что `slug` в списке полей `fields`, '
            'сериализатора модели Tag'
        )

