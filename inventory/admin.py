from django.contrib import admin
from .models import Product, Ingredient

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active']
    list_filter = ['category', 'is_active']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'stock_quantity', 'reorder_level']
