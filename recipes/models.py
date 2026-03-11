from django.db import models
from inventory.models import Ingredient


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Method, tips, fermentation times, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def total_weight_grams(self):
        """Sum of all ingredient amounts converted to grams."""
        total = 0
        for ri in self.recipe_ingredients.all():
            total += ri.amount_in_grams
        return round(total, 2)


class RecipeIngredient(models.Model):
    class Unit(models.TextChoices):
        GRAMS   = 'g',   'Grams (g)'
        POUNDS  = 'lb',  'Pounds (lb)'
        OUNCES  = 'oz',  'Ounces (oz)'

    GRAMS_PER_POUND = 453.592
    GRAMS_PER_OUNCE = 28.3495

    recipe     = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, related_name='recipe_uses')
    amount     = models.DecimalField(max_digits=10, decimal_places=3, help_text="Amount in the chosen unit")
    unit       = models.CharField(max_length=2, choices=Unit.choices, default=Unit.GRAMS)
    # Baker's percentage: ingredient weight / total flour weight * 100
    # Stored explicitly so bakers can enter it directly; kept in sync via the form/admin
    bakers_percentage = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True,
        help_text="Baker's percentage (ingredient ÷ total flour × 100)"
    )
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order in recipe")

    class Meta:
        ordering = ['order', 'ingredient__name']
        unique_together = [['recipe', 'ingredient']]

    def __str__(self):
        return f"{self.ingredient.name} — {self.amount}{self.unit}"

    @property
    def amount_in_grams(self):
        amt = float(self.amount)
        if self.unit == self.Unit.POUNDS:
            return amt * self.GRAMS_PER_POUND
        if self.unit == self.Unit.OUNCES:
            return amt * self.GRAMS_PER_OUNCE
        return amt

    def amount_display(self):
        """Returns a tidy string like '500 g' or '1.25 lb'."""
        amt = self.amount.normalize()
        return f"{amt} {self.get_unit_display().split(' ')[0]}"
