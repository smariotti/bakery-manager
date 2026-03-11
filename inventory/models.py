from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, help_text="e.g. kg, g, litres")
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.unit})"

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level


class Product(models.Model):
    class Category(models.TextChoices):
        BREAD  = 'bread',  'Bread'
        PASTRY = 'pastry', 'Pastry'
        CAKE   = 'cake',   'Cake'
        SAVORY = 'savory', 'Savory'
        OTHER  = 'other',  'Other'

    name     = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    description = models.TextField(blank=True)
    price    = models.DecimalField(max_digits=8, decimal_places=2)
    # Lazy import via string ref to avoid circular import
    recipe   = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products',
        help_text="The recipe used to make this product"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
