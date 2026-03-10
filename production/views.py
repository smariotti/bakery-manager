from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import ProductionBatch
from inventory.models import Product


def dashboard(request):
    today = timezone.now().date()
    todays_batches = ProductionBatch.objects.filter(production_date=today).select_related('product', 'assigned_to')
    ready_batches = ProductionBatch.objects.filter(status=ProductionBatch.Status.READY).select_related('product')
    context = {
        'todays_batches': todays_batches,
        'ready_batches': ready_batches,
        'today': today,
    }
    return render(request, 'production/dashboard.html', context)


def batch_list(request):
    batches = ProductionBatch.objects.select_related('product', 'assigned_to').order_by('-production_date')
    return render(request, 'production/batch_list.html', {'batches': batches})


def batch_detail(request, pk):
    batch = get_object_or_404(ProductionBatch, pk=pk)
    return render(request, 'production/batch_detail.html', {'batch': batch})


def batch_create(request):
    products = Product.objects.filter(is_active=True)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        product = get_object_or_404(Product, pk=product_id)
        batch = ProductionBatch.objects.create(
            product=product,
            quantity_planned=request.POST.get('quantity_planned'),
            production_date=request.POST.get('production_date'),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, f'Batch created for {product.name}.')
        return redirect('production:batch_detail', pk=batch.pk)
    return render(request, 'production/batch_form.html', {'products': products})


def batch_update_status(request, pk):
    batch = get_object_or_404(ProductionBatch, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ProductionBatch.Status.values:
            batch.status = new_status
            if new_status == ProductionBatch.Status.READY:
                batch.quantity_produced = request.POST.get('quantity_produced', batch.quantity_planned)
                batch.quantity_available = batch.quantity_produced
            batch.save()
            messages.success(request, f'Status updated to {batch.get_status_display()}.')
    return redirect('production:batch_detail', pk=pk)
