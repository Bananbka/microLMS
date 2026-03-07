from django.core.validators import MinValueValidator
from django.db import models


class AdjustmentCategory(models.TextChoices):
    BONUS = "BONUS", "Bonus"
    PENALTY = "PENALTY", "Penalty"


class PayoutAdjustment(models.Model):
    user = models.IntegerField()

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=24, choices=AdjustmentCategory.choices)

    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    payout = models.ForeignKey(
        'payroll.Payout',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='adjustments'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payroll_adjustments'
        ordering = ['-created_at']
