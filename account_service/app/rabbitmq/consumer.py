import pika
import json
from rabbitmq.connection import client_manager
from helpers.logger import logger


def process_transaction_created(ch, method, properties, body):
    data = json.loads(body)
    print(f"Received TransactionCreated event: {data}")
    logger.info(f"Received TransactionCreated event: {data}")
    # # Extract details
    # transaction_id = data['transaction_id']
    # account_id = data['account_id']
    # amount = data['amount']

    # # Update account (e.g., adjust balance)
    # update_account_balance(account_id, amount)

    # Acknowledge the message
    ch.basic_ack(delivery_tag=method.delivery_tag)


def update_account_balance(account_id, amount):
    # Logic to update account balance in the database
    print(f"Updating balance for Account {account_id} by {amount}")


def start_consumer():

    channel = client_manager.get_channel()

    # Declare exchange and queue
    channel.exchange_declare(
        exchange="transactions.events", exchange_type="topic", durable=True
    )
    channel.queue_declare(queue="accounts.transactions", durable=True)

    # Bind queue to exchange
    channel.queue_bind(
        exchange="transactions.events",
        queue="accounts.transactions",
        routing_key="transaction.created",
    )

    # Start consuming
    channel.basic_consume(
        queue="accounts.transactions", on_message_callback=process_transaction_created
    )
    print("Waiting for TransactionCreated events...")
    channel.start_consuming()
