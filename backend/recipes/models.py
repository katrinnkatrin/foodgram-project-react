from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """ Модель для тегов. """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название тега'
    )
    color = models.CharField(
        max_length=17,
        unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Идентификатор тега'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Модель для ингредиентов. """
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Модель для рецептов. """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Фото рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты, используемые в рецепте'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги, используемые для рецепта'
    )
    cooking_time = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1, 'Приготовление от 1 минут'),
        ],
        verbose_name='Время приготовления в минутах',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:10]


class RecipeIngredient(models.Model):
    """ Модель для связи ингредиентов с рецептами. """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Описание рецепта'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1, 'Минимальное количество = 1'), ],
        verbose_name='Количество'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['ingredient', 'recipe'], name='unique_recipe_ingredient')]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return 'Ингридиент в рецепте'


class RecipeTag(models.Model):
    """ Модель для связи тегов с рецептами. """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Название рецепта'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег рецепта'
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['tag', 'recipe'],
                                               name='unique_recipe_tag')]
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'

    def __str__(self):
        return 'Тег рецепта'


class Favorite(models.Model):
    """ Модель для избранных рецептов. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_user_favorite'
        )]
        ordering = ('-id',)
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'


class ShoppingList(models.Model):
    """ Модель для списка покупок. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_shopping_cart'
        )]
        ordering = ('-id',)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
