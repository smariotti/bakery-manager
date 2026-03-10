from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['batch', 'quantity_sold', 'channel', 'sale_date', 'sold_by']
    list_filter = ['channel', 'sale_date']
