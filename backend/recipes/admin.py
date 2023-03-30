from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from api.recipes.filters import FirstLetterFilter
from recipes.models import Ingredient, Tag, Recipe, RecipeIngredient
from users.models import User


class UserAdminCustom(admin.ModelAdmin):
    list_filter = ('email', 'username', )


class TagAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', )
    list_filter = (FirstLetterFilter, )


class RecipeIngredientFormSet(BaseInlineFormSet):
    """Кастомный формсет для админки, чтобы через админку нельзя было
     создать рецепт без ингредиентов."""
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        count = 0
        for ingredient in self.cleaned_data:
            if ingredient and not ingredient.get('DELETE', False):
                count += 1
        if count == 0:
            raise ValidationError('А где ингредиенты, профессор?')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    formset = RecipeIngredientFormSet


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('count_favorites', )
    list_display = ('name', 'author', )
    list_filter = (FirstLetterFilter, 'tags', 'author', )
    inlines = (RecipeIngredientInline, )

    def count_favorites(self, obj):
        return obj.favorited.count()

    count_favorites.short_description = 'Количество добавлений в избранное'


admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
