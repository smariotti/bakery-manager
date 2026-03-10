from django.db import models
from django.contrib.auth.models import User
from production.models import ProductionBatch


class Sale(models.Model):
    class Channel(models.TextChoices):
        COUNTER = 'counter', 'Counter'
        WHOLESALE = 'wholesale', 'Wholesale'
        ONLINE = 'online', 'Online'
        OTHER = 'other', 'Other'

    batch = models.ForeignKey(ProductionBatch, on_delete=models.PROTECT, related_name='sales')
    quantity_sold = models.PositiveIntegerField()
    channel = models.CharField(max_length=20, choices=Channel.choices, default=Channel.COUNTER)
    sold_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales'
    )
    sale_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-sale_date']

    def __str__(self):
        return f"{self.batch.product.name} x{self.quantity_sold} — {self.sale_date:%Y-%m-%d %H:%M}"

    @property
    def total_value(self):
        return self.quantity_sold * self.batch.product.price
