from django.core.validators import MinValueValidator
from django.db import models


class PayoutStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class Payout(models.Model):
    user = models.IntegerField()

    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(max_length=20, choices=PayoutStatus.choices, default=PayoutStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payroll_payouts'
        ordering = ['-created_at']