from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.recipes.filters import RecipeFilter
from api.recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
)
from api.users.serializers import MiniRecipeSerializer
from recipes.models import (
    Ingredient, Tag, Recipe, RecipeFavorite, RecipeInCart
)
from tools.common import draw_pdf


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (AllowAny, )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    lookup_field = 'id'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        RecipeFavorite.objects.get_or_create(recipe=recipe, user=user)
        serializer = MiniRecipeSerializer(instance=recipe)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def unfavorite(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        favorite = RecipeFavorite.objects.filter(
            recipe=recipe, user=user
        )
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('В вашем списке избранного нет этого рецепта.',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart'
    )
    def add_to_cart(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        RecipeInCart.objects.get_or_create(recipe=recipe, user=user)
        serializer = MiniRecipeSerializer(instance=recipe)
        return Response(serializer.data, status.HTTP_201_CREATED)

    @add_to_cart.mapping.delete
    def remove_from_cart(self, request, **kwargs):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        recipe_in_cart = RecipeInCart.objects.filter(
            recipe=recipe, user=user
        )
        if recipe_in_cart:
            recipe_in_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('В вашем списке покупок нет этого рецепта.',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        queryset = Ingredient.objects.filter(
            recipeingredient__recipe__in_cart__user=self.request.user
        ).values(
            'name', 'measurement_unit'
        ).annotate(amount=Sum('recipeingredient__amount'))
        shopping_list = [
            f'{item["name"]} ({item["measurement_unit"]}) — {item["amount"]}'
            for item in queryset
        ]
        result = draw_pdf(shopping_list)
        return FileResponse(
            result,
            as_attachment=True,
            filename='shopping_list.pdf'
        )
