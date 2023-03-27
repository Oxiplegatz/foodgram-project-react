from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, BooleanFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Фильтр для рецептов. Фильтрует рецепты по тегам, а также
     используется для показа рецептов в избранном и списке покупок."""
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_favorited = BooleanFilter(
        field_name='favorited',
        method='check_favorite'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='in_cart',
        method='check_shopping_cart'
    )

    class Meta:
        fields = ('tags', )
        model = Recipe

    def check_favorite(self, queryset, name, value):
        lookup = '__'.join([name, 'user'])
        return queryset.filter(**{lookup: self.request.user})

    def check_shopping_cart(self, queryset, name, value):
        lookup = '__'.join([name, 'user'])
        return queryset.filter(**{lookup: self.request.user})
