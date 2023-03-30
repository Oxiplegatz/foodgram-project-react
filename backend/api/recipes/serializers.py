import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from api.users.serializers import UserSerializer
from recipes.models import Ingredient, Recipe, Tag, RecipeIngredient


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )
        read_only_fields = ('__all__', )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )
        read_only_fields = ('__all__', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount', )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.ingredient.id
        return representation


class RecipeSerializer(serializers.ModelSerializer):
    """Основной сериализатор рецептов."""
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(required=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True, read_only=True)
        return super().to_representation(instance)

    def get_or_update_ingredients(self, recipe, ingredients):
        current_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        if current_ingredients:
            current_ingredients.delete()
        for ingredient in ingredients:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.get_or_update_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        self.get_or_update_ingredients(instance, ingredients)
        instance.save()
        return instance

    def get_is_favorited(self, obj):
        user = self.context['view'].request.user
        if not user.is_authenticated:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['view'].request.user
        if not user.is_authenticated:
            return False
        return user.recipes_in_cart.filter(recipe=obj).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        if not ingredients:
            raise ValidationError({'ingredients': 'Не указаны ингредиенты.'})
        if not tags:
            raise ValidationError({'tags': 'Не указаны id тегов.'})

        unique_ingredients = []
        for item in ingredients:
            unique_ingredients.append(item['id'])
        if len(set(unique_ingredients)) < len(ingredients):
            raise ValidationError(
                'Ингредиенты в рецепте не могут повторяться.'
            )

        return data
