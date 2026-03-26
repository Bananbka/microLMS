import json
import pika
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.payroll.infrastructure.models import Payout, PayoutAdjustment, AdjustmentCategory, OutboxEvent


class Command(BaseCommand):
    def handle(self, *args, **options):
        broker_url = settings.CELERY_BROKER_URL.rstrip('/') + '/%2F'

        connection = pika.BlockingConnection(pika.URLParameters(broker_url))
        channel = connection.channel()

        channel.exchange_declare(
            exchange='microLMS_events',
            exchange_type='topic',
            durable=True
        )

        result = channel.queue_declare(queue='payroll_events_queue', durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='microLMS_events', queue=queue_name, routing_key='user.purchase.validated')

        def callback(ch, method, properties, body):
            event = json.loads(body)
            routing_key = method.routing_key

            self.stdout.write(self.style.SUCCESS(f"Got the EVENT: {event['event_type']}"))

            if routing_key == 'user.purchase.validated':
                payload = event['payload']
                self.stdout.write(f"Payroll: transferring money to author {payload['author_id']}")

                PayoutAdjustment.objects.create(
                    user=payload['author_id'],
                    name=f"Sale of course {payload['course_id']}",
                    amount=payload['price'],
                    category=AdjustmentCategory.BONUS,
                )

                OutboxEvent.objects.create(
                    event_type='PayrollTransferSuccess',
                    routing_key='payroll.transfer.success',
                    payload={
                        "purchase_id": payload['purchase_id'],
                        "status": "SUCCESS"
                    }
                )

                self.stdout.write(f"Payroll: transfer completed for purchase {payload['purchase_id']}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        self.stdout.write(self.style.SUCCESS('Payroll Consumer is launched. Waiting for...'))
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()
