from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (Tag, Ingredient, Recipe,
                            RecipeIngredient, Favorite, ShoppingList)
from recipes.serializers import (TagsSerializer, IngredientsSerializer,
                                 ShowRecipeFullSerializer, AddRecipeSerializer,
                                 FavoriteSerializer, ShoppingListSerializer)     
from recipes.filters import IngredientsFilter, RecipeFilter
from recipes.mixins import RetriveAndListViewSet
from recipes.permissions import IsAuthorOrAdmin
from recipes.utils import download_file_response
from users.paginator import CustomPaginator

User = get_user_model()

class TagsViewSet(RetriveAndListViewSet):
    """ Вьюсет для тегов. """
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class IngredientsViewSet(RetriveAndListViewSet):
    """ Вьюсет для ингредиентов. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вьюсет для рецептов. """
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = [IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPaginator
    http_method_names = ('get', 'post', 'patch', 'delete', 'put')
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ShowRecipeFullSerializer
        return AddRecipeSerializer

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.bulk_create([
                RecipeIngredient(            
                    recipe=recipe,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
            ])

    def perform_create(self, serializer):
        author = self.request.user
        image = serializer.validated_data.pop('image')
        ingredients = serializer.validated_data.pop('ingredients')
        recipe = serializer.save(image=image, author=author)
        self.create_ingredients(ingredients, recipe)

    def perform_update(self, serializer):
        data = serializer.validated_data
        ingredients = data.pop('ingredients')
        instance = serializer.save()
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        
            
    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='favorite',
        permission_classes=[IsAuthorOrAdmin],
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Этот рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = Favorite.objects.create(user=user, recipe=recipe)
            serializer = FavoriteSerializer(favorite,
                                            context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='shopping_cart',
        permission_classes=[IsAuthorOrAdmin],
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if ShoppingList.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Этот рецепт уже в корзине покупок!'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shoping_cart = ShoppingList.objects.create(user=user,
                                                       recipe=recipe)
            serializer = ShoppingListSerializer(
                shoping_cart, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            delete_shoping_cart = ShoppingList.objects.filter(user=user,
                                                              recipe=recipe)
            if delete_shoping_cart.exists():
                delete_shoping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients_list = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        if ingredients_list == []:
            return Response(
                {'error': 'В рецепте нет ингредиентов!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return download_file_response(ingredients_list)
            



