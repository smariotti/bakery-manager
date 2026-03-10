from django.contrib import admin
from .models import ProductionBatch

@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = ['product', 'production_date', 'quantity_planned', 'quantity_available', 'status']
    list_filter = ['status', 'production_date']
    search_fields = ['product__name']
