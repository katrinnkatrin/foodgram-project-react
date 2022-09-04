from django.contrib.admin import ModelAdmin, register

from .models import Ingredient, IngredientAmount, Recipe, Tag, Shopping_Cart, Favorite_Recipe


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color')


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('count_favorites',)

    def count_favorites(self, obj):
        return obj.favorites.count()

    count_favorites.short_description = 'Число добавлений в избранное'


@register(IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):
    pass


@register(Favorite_Recipe)
class FavoriteAdmin(ModelAdmin):
    pass


@register(Shopping_Cart)
class CartAdmin(ModelAdmin):
    pass
