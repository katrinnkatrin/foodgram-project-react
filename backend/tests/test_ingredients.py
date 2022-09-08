import pytest

from recipes.models import Ingredient


class TestIngredientAPI:
    url_ingr = '/api/ingredients/'

    @pytest.mark.django_db(transaction=True)
    def test_ingredient_not_authenticated(self, client):
        response = client.get(f'{self.url_ingr}')

        code = 200
        assert response.status_code == code, (
            f'Анонимный пользователь при get запросе {self.url_ingr}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_ingredient_authenticated(self, user_client):
        response = user_client.get(f'{self.url_ingr}')

        code = 200
        assert response.status_code == code, (
            f'Авторизованный пользователь при get запросе `{self.url_ingr}` '
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_ingredient_id_authenticated(self, user_client, ingredient_1):
        response = user_client.get(f'{self.url_ingr}{ingredient_1.id}/')

        code = 200
        assert response.status_code == code, (
            f'Авторизованный пользователь при get запросе '
            f'- на {self.url_ingr}{ingredient_1.id}/'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_ingredient_id_not_authenticated(self, client, ingredient_1):
        response = client.get(f'{self.url_ingr}{ingredient_1.id}/')

        code = 200
        assert response.status_code == code, (
            f'Анонимный пользователь при get запросе '
            f'- на {self.url_ingr}{ingredient_1.id}/'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_ingredient_get(self, user_client, ingredient_1, ingredient_2):
        response = user_client.get(f'{self.url_ingr}')

        test_data = response.json()
        assert type(test_data) == dict, (
            f'При GET запросе на {self.url_ingr} должен вернуться словарь'
        )

        assert len(test_data['results']) == Ingredient.objects.all().count(), (
            'При GET запросе должен возвращаться весь список'
        )

        test_ingredient = test_data['results'][0]
        assert 'id' in test_ingredient, (
            'Проверить, что `id` в списке полей `fields`, '
            'сериализатора модели Ingredient'
        )

        assert 'name' in test_ingredient, (
            'Проверить, что `name` в списке полей `fields`, '
            'сериализатора модели Ingredient'
        )

        assert 'measurement_unit' in test_ingredient, (
            'Проверить, что `measurement_unit` в списке полей `fields`, '
            'сериализатора модели Ingredient'
        )
