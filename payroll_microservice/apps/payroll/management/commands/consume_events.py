import json
import pika
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.payroll.infrastructure.models import Payout


class Command(BaseCommand):
    def handle(self, *args, **options):
        broker_url = settings.CELERY_BROKER_URL.rstrip('/') + '/%2F'

        connection = pika.BlockingConnection(pika.URLParameters(broker_url))
        channel = connection.channel()

        channel.exchange_declare(
            exchange='microLMS_events',
            exchange_type='fanout',
            durable=True
        )

        result = channel.queue_declare(queue='payroll_events_queue', durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='microLMS_events', queue=queue_name)

        def callback(ch, method, properties, body):
            event = json.loads(body)
            self.stdout.write(self.style.SUCCESS(f"Got the EVENT: {event['event_type']}"))

            if event['event_type'] == 'UserCreated':
                payload = event['payload']
                self.stdout.write(f"Payroll: creating payroll for new user {payload['email']}")
                Payout.objects.create(user=payload['user_id'], amount=0)
                self.stdout.write(f"Payroll: payroll was created {payload['email']}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        self.stdout.write(self.style.SUCCESS('Payroll Consumer is launched. Waiting for...'))
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()
