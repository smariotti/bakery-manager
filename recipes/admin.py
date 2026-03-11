from django.contrib import admin
from .models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 3
    fields = ['order', 'ingredient', 'amount', 'unit', 'bakers_percentage']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_weight_grams', 'updated_at']
    search_fields = ['name']
    inlines = [RecipeIngredientInline]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'amount', 'unit', 'bakers_percentage']
    list_filter = ['recipe', 'unit']
