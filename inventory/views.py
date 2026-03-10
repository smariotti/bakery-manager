from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Ingredient


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'inventory/product_list.html', {'products': products})


def product_create(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            description=request.POST.get('description', ''),
            price=request.POST['price'],
        )
        messages.success(request, 'Product created.')
        return redirect('inventory:product_list')
    return render(request, 'inventory/product_form.html', {'categories': Product.Category.choices})


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
