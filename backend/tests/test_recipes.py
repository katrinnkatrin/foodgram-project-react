import pytest

from recipes.models import Recipe


class TestRecipeAPI:
    url_recipe = '/api/recipes/'

    @pytest.mark.django_db(transaction=True)
    def test_recipe_not_authenticated(self, client):
        response = client.get(f'{self.url_recipe}')

        code = 200
        assert response.status_code == code, (
            f'Анонимный пользователь при get запросе {self.url_recipe}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe_not_authenticated(self, client):
        response = client.post(f'{self.url_recipe}')

        code = 401
        assert response.status_code == code, (
            f'Анонимный пользователь при post запросе {self.url_recipe}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_authenticated(self, user_client):
        response = user_client.get(f'{self.url_recipe}')

        code = 200
        assert response.status_code == code, (
            f'Авторизованный пользователь при get запросе {self.url_recipe}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_recipe_authenticated(self, user_client):
        response = user_client.get(f'{self.url_recipe}')

        code = 200
        assert response.status_code == code, (
            f'Авторизованный пользователь при post запросе {self.url_recipe}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipe_get(self, user_client, recipe_1, recipe_2):
        response = user_client.get(f'{self.url_recipe}')

        test_data = response.json()
        assert type(test_data) == dict, (
            f'При GET запросе на {self.taurl_recipegs} должен вернуться словарь'
        )

        assert len(test_data['results']) == Recipe.objects.all().count(), (
            'При GET запросе должен возвращаться весь список'
        )

        test_recipe = test_data['results'][0]
        assert 'id' in test_recipe, (
            'Проверить, что `id` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'tags' in test_recipe, (
            'Проверить, что `tags` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'author' in test_recipe, (
            'Проверить, что `author` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'ingredients' in test_recipe, (
            'Проверить, что `ingredients` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'is_favorited' in test_recipe, (
            'Проверить, что `is_favorited` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'is_in_shopping_cart' in test_recipe, (
            'Проверить, что `is_in_shopping_cart` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'name' in test_recipe, (
            'Проверить, что `name` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'image' in test_recipe, (
            'Проверить, что `image` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'text' in test_recipe, (
            'Проверить, что `text` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )

        assert 'cooking_time' in test_recipe, (
            'Проверить, что `cooking_time` в списке полей `fields`, '
            'сериализатора модели Recipe'
        )
