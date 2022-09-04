import pytest


class TestFavoritetAPI:
    favorite = '/favorite/'
    url_recipe = '/api/recipes/'

    @pytest.mark.django_db(transaction=True)
    def test_favorite_add_not_authenticated(self, client, recipe_1):
        response = client.post(
            f'{self.url_recipe}{recipe_1.id}{self.favorite}')

        code = 401
        assert response.status_code == code, (
            'Анонимный пользователь при post запросе'
            f'- на {self.url_recipe}{recipe_1.id}{self.favorite}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_add_authenticated(self, user_client, recipe_1):
        response = user_client.post(
            f'{self.url_recipe}{recipe_1.id}{self.favorite}')

        code = 201
        assert response.status_code == code, (
            'Авторизованный пользователь при post запросе'
            f'- на {self.url_recipe}{recipe_1.id}{self.favorite}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_add_again_authenticated(self, user_client, recipe_1):
        user_client.post(f'{self.url_recipe}{recipe_1.id}{self.favorite}')
        response = user_client.post(
            f'{self.url_recipe}{recipe_1.id}{self.favorite}')

        code = 400
        assert response.status_code == code, (
            'При повторном добавлении рецепта в избранное, '
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_del_add_not_authenticated(self, client, recipe_1):
        response = client.delete(
            f'{self.url_recipe}{recipe_1.id}{self.favorite}')

        code = 401
        assert response.status_code == code, (
            'Анонимный пользователь при del запросе'
            f'- на {self.url_recipe}{recipe_1.id}{self.favorite}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_del_authenticated(self, user_client, recipe_1):
        user_client.post(f'{self.url_recipe}{recipe_1.id}{self.favorite}')
        response = user_client.delete(
            f'{self.url_recipe}{recipe_1.id}{self.favorite}')

        code = 204
        assert response.status_code == code, (
            'Авторизованный пользователь при del запросе'
            f'- на {self.url_recipe}{recipe_1.id}{self.favorite}'
            f'должен получать ответ с кодом {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_del_again_authenticated(self, user_client, recipe_1):
        user_client.post(f'{self.url_recipe}{recipe_1.id}')
        user_client.delete(f'{self.url_recipe}{recipe_1.id}')
        response = user_client.delete(
            f'{self.url_recipe}{recipe_1.id}{self.favorite}')

        code = 400
        assert response.status_code == code, (
            'При повторном удалении рецепта из избранного, '
            f'должен получать ответ с кодом {code}'
        )
