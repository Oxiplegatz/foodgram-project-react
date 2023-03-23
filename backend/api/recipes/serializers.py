import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

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

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', )


class RecipeDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, required=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Tag.objects.all()
    )
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients_data:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        return recipe


# class RecipeListSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     tags = TagRecipeDetailSerializer(many=True, required=True, allow_null=True)
#     ingredients = IngredientRecipeDetailSerializer(many=True, required=True)
#     image = Base64ImageField(required=True)
#     is_favorited = SerializerMethodField()
#     is_in_shopping_cart = SerializerMethodField()
#
#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'author',
#             'ingredients',
#             'tags',
#             'is_favorited',
#             'is_in_shopping_cart',
#             'image',
#             'name',
#             'text',
#             'cooking_time',
#         )
#         depth = 1
#
#     def get_is_favorited(self):
#         return False
#
#     def get_is_in_shopping_cart(self):
#         return False
