from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Recipe, RecipeIngredient
from inventory.models import Ingredient


def recipe_list(request):
    recipes = Recipe.objects.prefetch_related('recipe_ingredients__ingredient', 'products').all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.prefetch_related('recipe_ingredients__ingredient', 'products'),
        pk=pk
    )
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


def recipe_create(request):
    ingredients = Ingredient.objects.all()
    if request.method == 'POST':
        recipe = _save_recipe(request, None)
        if recipe:
            messages.success(request, f'Recipe "{recipe.name}" created.')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
    return render(request, 'recipes/recipe_form.html', {
        'ingredients': ingredients,
        'units': RecipeIngredient.Unit.choices,
        'recipe': None,
    })


def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = Ingredient.objects.all()
    if request.method == 'POST':
        updated = _save_recipe(request, recipe)
        if updated:
            messages.success(request, f'Recipe "{updated.name}" updated.')
            return redirect('recipes:recipe_detail', pk=updated.pk)
    return render(request, 'recipes/recipe_form.html', {
        'ingredients': ingredients,
        'units': RecipeIngredient.Unit.choices,
        'recipe': recipe,
    })


@transaction.atomic
def _save_recipe(request, recipe):
    """Shared create/update logic. Returns Recipe on success, None on error."""
    name = request.POST.get('name', '').strip()
    if not name:
        messages.error(request, 'Recipe name is required.')
        return None

    if recipe is None:
        recipe = Recipe(name=name)
    else:
        recipe.name = name

    recipe.description = request.POST.get('description', '')
    recipe.notes = request.POST.get('notes', '')
    recipe.save()

    # Rebuild all recipe ingredients from the dynamic rows
    recipe.recipe_ingredients.all().delete()

    ingredient_ids  = request.POST.getlist('ingredient_id')
    amounts         = request.POST.getlist('amount')
    units           = request.POST.getlist('unit')
    bakers_pcts     = request.POST.getlist('bakers_percentage')
    orders          = request.POST.getlist('order')

    for i, ing_id in enumerate(ingredient_ids):
        if not ing_id or not amounts[i]:
            continue
        try:
            ingredient = Ingredient.objects.get(pk=ing_id)
        except Ingredient.DoesNotExist:
            continue

        bp_raw = bakers_pcts[i] if i < len(bakers_pcts) else ''
        bp = float(bp_raw) if bp_raw.strip() else None
        order = int(orders[i]) if i < len(orders) and orders[i].strip().isdigit() else i

        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amounts[i],
            unit=units[i] if i < len(units) else RecipeIngredient.Unit.GRAMS,
            bakers_percentage=bp,
            order=order,
        )

    return recipe
