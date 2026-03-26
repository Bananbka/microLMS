from celery import shared_task
import pika
import json
from django.conf import settings

from apps.courses.infrastructure.models import OutboxEvent


@shared_task
def publish_outbox_events():
    events = OutboxEvent.objects.filter(status='PENDING')

    if not events.exists():
        return "No pending events"

    broker_url = settings.CELERY_BROKER_URL.rstrip('/') + '/%2F'

    connection = pika.BlockingConnection(pika.URLParameters(broker_url))
    channel = connection.channel()

    channel.exchange_declare(
        exchange='microLMS_events',
        exchange_type='topic',
        durable=True
    )

    processed_count = 0
    for event in events:
        try:
            message = {
                "event_id": event.id,
                "event_type": event.event_type,
                "payload": event.payload,
                "timestamp": event.created_at.isoformat()
            }

            channel.basic_publish(
                exchange='microLMS_events',
                routing_key=event.routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )

            event.status = 'PROCESSED'
            event.save(update_fields=['status'])
            processed_count += 1

        except Exception as e:
            event.status = 'FAILED'
            event.save(update_fields=['status'])

    connection.close()
    return f"Processed {processed_count} events"
