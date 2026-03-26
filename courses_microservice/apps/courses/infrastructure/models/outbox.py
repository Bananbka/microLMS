from django.db import models


class OutboxEventStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSED = 'PROCESSED', 'Processed'
    FAILED = 'FAILED', 'Failed'


class OutboxEvent(models.Model):
    event_type = models.CharField(max_length=255)
    routing_key = models.CharField(max_length=255)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=OutboxEventStatus.choices, default=OutboxEventStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_outbox_events'
        ordering = ['created_at']
