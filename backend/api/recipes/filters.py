from django.contrib import admin
from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, BooleanFilter

from recipes.models import Recipe, Tag

ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'


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


class FirstLetterFilter(admin.SimpleListFilter):
    """Алфавитный фильтр элементов по первой букве для админки."""
    title = 'Первая буква названия'
    parameter_name = 'letter'
    letters = list(ALPHABET)

    def lookups(self, request, model_admin):
        queryset = model_admin.get_queryset(request)
        lookups = []
        for letter in self.letters:
            count = queryset.filter(name__istartswith=letter).count()
            if count:
                lookups.append((letter, f'{letter} ({count})'))
        return lookups

    def queryset(self, request, queryset):
        if self.value() in self.letters:
            return queryset.filter(name__istartswith=self.value())
