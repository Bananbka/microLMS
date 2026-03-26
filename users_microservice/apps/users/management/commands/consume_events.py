import json
import pika
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.users.infrastructure.models import User, OutboxEvent


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

        result = channel.queue_declare(queue='users_events_queue', durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='microLMS_events', queue=queue_name, routing_key='course.purchase.initiated')

        def callback(ch, method, properties, body):
            event = json.loads(body)
            routing_key = method.routing_key

            self.stdout.write(self.style.SUCCESS(f"Got EVENT from route [{routing_key}]: {event['event_type']}"))

            if routing_key == 'course.purchase.initiated':
                payload = event['payload']
                user_id = payload['user_id']

                try:
                    user = User.objects.get(id=user_id)

                    if not user.is_active:
                        raise ValueError("User account is inactive or blocked.")

                    self.stdout.write(f"Users: Validated user {user_id}. Moving forward.")

                    OutboxEvent.objects.create(
                        event_type='UserPurchaseValidated',
                        routing_key='user.purchase.validated',
                        payload=payload
                    )

                except (User.DoesNotExist, ValueError) as e:
                    self.stdout.write(
                        self.style.ERROR(f"Users: Validation failed for user {user_id}. Reason: {str(e)}"))

                    OutboxEvent.objects.create(
                        event_type='UserPurchaseFailed',
                        routing_key='user.purchase.failed',
                        payload={
                            "purchase_id": payload['purchase_id'],
                            "reason": str(e)
                        }
                    )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        self.stdout.write(self.style.SUCCESS('Users Consumer is launched. Waiting for events...'))
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()
