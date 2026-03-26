import json
import time
import pika
from pika.exceptions import AMQPConnectionError
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.courses.infrastructure.models import CoursePurchase


class Command(BaseCommand):
    def handle(self, *args, **options):
        broker_url = settings.CELERY_BROKER_URL.rstrip('/') + '/%2F'

        connection = None
        retries = 10

        while retries > 0:
            try:
                self.stdout.write("Connecting to RabbitMQ...")
                connection = pika.BlockingConnection(pika.URLParameters(broker_url))
                break
            except AMQPConnectionError:
                retries -= 1
                self.stdout.write(self.style.WARNING(f"RabbitMQ not ready. Retrying... ({retries} left)"))
                time.sleep(5)

        if not connection:
            self.stdout.write(self.style.ERROR("Could not connect to RabbitMQ. Exiting."))
            return

        channel = connection.channel()

        channel.exchange_declare(
            exchange='microLMS_events',
            exchange_type='topic',
            durable=True
        )

        result = channel.queue_declare(queue='courses_events_queue', durable=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange='microLMS_events', queue=queue_name, routing_key='payroll.transfer.success')
        channel.queue_bind(exchange='microLMS_events', queue=queue_name, routing_key='payroll.transfer.failed')
        channel.queue_bind(exchange='microLMS_events', queue=queue_name, routing_key='user.purchase.failed')

        def callback(ch, method, properties, body):
            event = json.loads(body)
            routing_key = method.routing_key
            payload = event['payload']
            purchase_id = payload.get('purchase_id')

            self.stdout.write(self.style.SUCCESS(f"Got EVENT from route [{routing_key}] for purchase {purchase_id}"))

            if not purchase_id:
                self.stdout.write(self.style.ERROR("Event is missing purchase_id!"))
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return

            try:
                purchase = CoursePurchase.objects.get(id=purchase_id)

                if routing_key == 'payroll.transfer.success':
                    purchase.status = 'SUCCESS'
                    purchase.save(update_fields=['status'])
                    self.stdout.write(
                        f"Courses: Access granted to user {purchase.user_id} for course {purchase.course_id}!")

                elif routing_key in ['payroll.transfer.failed', 'user.purchase.failed']:
                    purchase.status = 'FAILED'
                    purchase.error_message = payload.get('reason', 'Unknown error')
                    purchase.save(update_fields=['status', 'error_message'])
                    self.stdout.write(self.style.WARNING(
                        f"Courses: Purchase failed. Status reverted to FAILED. Reason: {purchase.error_message}"))

            except CoursePurchase.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Courses: Purchase {purchase_id} not found in DB!"))

            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        self.stdout.write(self.style.SUCCESS('Courses Consumer is launched. Waiting for events...'))
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        connection.close()