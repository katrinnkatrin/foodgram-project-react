import pytest


@pytest.fixture
def tag_1():
    from recipes.models import Tag
    return Tag.objects.create(name='Таг_1', color='#E26C2D', slug='Группа_1')


@pytest.fixture
def tag_2():
    from recipes.models import Tag
    return Tag.objects.create(name='Таг_2', color='#FF0000', slug='Группа_2')


@pytest.fixture
def ingredient_1():
    from recipes.models import Ingredient
    return Ingredient.objects.create(
        name='Ингредиент_1', measurement_unit='г.')


@pytest.fixture
def ingredient_2():
    from recipes.models import Ingredient
    return Ingredient.objects.create(
        name='Ингредиент_2', measurement_unit='г.')


@pytest.fixture
def recipe_1():
    from recipes.models import Recipe
    recipe = Recipe.objects.create(
        name='string1', text='string', cooking_time=1
    )
    return recipe


@pytest.fixture
def recipe_2():
    from recipes.models import Recipe
    recipe = Recipe.objects.create(
        name='string2', text='string', cooking_time=2
    )
    return recipe
