from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticated

from api.recipes.serializers import (
    TagSerializer, IngredientSerializer, RecipeDetailSerializer
)
from recipes.models import Ingredient, Tag, Recipe


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = (IsAuthenticated, )
    ordering = ('pub_date', )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
