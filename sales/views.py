from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Sale
from production.models import ProductionBatch


def sale_list(request):
    sales = Sale.objects.select_related('batch__product', 'sold_by').order_by('-sale_date')
    return render(request, 'sales/sale_list.html', {'sales': sales})


def sale_create(request, batch_id):
    batch = get_object_or_404(ProductionBatch, pk=batch_id)
    if request.method == 'POST':
        qty = int(request.POST['quantity_sold'])
        if qty > batch.quantity_available:
            messages.error(request, f'Only {batch.quantity_available} available.')
        else:
            Sale.objects.create(
                batch=batch,
                quantity_sold=qty,
                channel=request.POST.get('channel', Sale.Channel.COUNTER),
                notes=request.POST.get('notes', ''),
                sold_by=request.user if request.user.is_authenticated else None,
            )
            batch.quantity_available -= qty
            if batch.quantity_available == 0:
                batch.status = ProductionBatch.Status.SOLD_OUT
            batch.save()
            messages.success(request, f'Sale recorded: {qty}x {batch.product.name}.')
            return redirect('production:dashboard')
    return render(request, 'sales/sale_form.html', {
        'batch': batch,
        'channels': Sale.Channel.choices,
    })
