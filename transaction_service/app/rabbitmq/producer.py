import pika
import json
from rabbitmq.connection import client_manager


def publish_transaction_created(message: str):
    channel = client_manager.get_channel()

    # Declare exchange
    channel.exchange_declare(
        exchange="transactions.events", exchange_type="topic", durable=True
    )

    # # Publish message
    # message = {
    #     'transaction_id': transaction_id,
    #     'account_id': account_id,
    #     'amount': amount
    # }

    channel.basic_publish(
        exchange="transactions.events",
        routing_key="transaction.created",
        body=json.dumps(message),
        properties=pika.BasicProperties(
            content_type="application/json", delivery_mode=2
        ),
    )

    print(f"Published TransactionCreated event: {message}")
