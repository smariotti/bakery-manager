from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Ingredient


def product_list(request):
    products = Product.objects.filter(is_active=True).select_related('recipe').prefetch_related('recipe__recipe_ingredients__ingredient')
    return render(request, 'inventory/product_list.html', {'products': products})


def product_create(request):
    from recipes.models import Recipe
    recipes = Recipe.objects.all()
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe') or None
        recipe = None
        if recipe_id:
            try:
                recipe = Recipe.objects.get(pk=recipe_id)
            except Recipe.DoesNotExist:
                pass
        Product.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            description=request.POST.get('description', ''),
            price=request.POST['price'],
            recipe=recipe,
        )
        messages.success(request, 'Product created.')
        return redirect('inventory:product_list')
    return render(request, 'inventory/product_form.html', {
        'categories': Product.Category.choices,
        'recipes': recipes,
    })


def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'inventory/ingredient_list.html', {'ingredients': ingredients})


def ingredient_create(request):
    if request.method == 'POST':
        Ingredient.objects.create(
            name=request.POST['name'],
            unit=request.POST['unit'],
            stock_quantity=request.POST.get('stock_quantity', 0),
            reorder_level=request.POST.get('reorder_level', 0),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Ingredient added.')
        return redirect('inventory:ingredient_list')
    return render(request, 'inventory/ingredient_form.html')
