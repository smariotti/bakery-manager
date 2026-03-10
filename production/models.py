from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product


class ProductionBatch(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Planned'
        MIXING = 'mixing', 'Mixing'
        SHAPING = 'shaping', 'Shaping'
        PROOFING = 'proofing', 'Proofing'
        BAKING = 'baking', 'Baking'
        COOLING = 'cooling', 'Cooling'
        READY = 'ready', 'Ready'
        SOLD_OUT = 'sold_out', 'Sold Out'

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='batches')
    quantity_planned = models.PositiveIntegerField()
    quantity_produced = models.PositiveIntegerField(default=0)
    quantity_available = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    production_date = models.DateField()
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='batches'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-production_date', 'product']
        verbose_name_plural = 'Production Batches'

    def __str__(self):
        return f"{self.product.name} — {self.production_date} ({self.get_status_display()})"
