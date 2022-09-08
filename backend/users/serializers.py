from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer


from recipes.models import Recipe
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """ Сериализатор для пользователя. """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta():
        model = User
        fields = ('id', 'email', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=self.context['request'].user,
                                     author=obj).exists()


class UserRegistrationSerializer(UserCreateSerializer):
    """ Сериализатор для регистрации пользователя. """
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password')


class FollowingRecipesSerializers(serializers.ModelSerializer):
    """ Сериализатор для подписки на рецепт. """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowFollowSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения подписки. """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        return Follow.objects.filter(
            author=obj, user=self.context['request'].user).exists()

    def get_recipes(self, obj):
        recipes_limit = int(self.context['request'].GET.get(
            'recipes_limit', 10))
        user = get_object_or_404(User, pk=obj.pk)
        recipes = Recipe.objects.filter(author=user)[:recipes_limit]

        return FollowingRecipesSerializers(recipes, many=True).data

    def get_recipes_count(self, obj):
        user = get_object_or_404(User, pk=obj.pk)
        return Recipe.objects.filter(author=user).count()
