import os
import pika
import sys
import json
from datetime import datetime


def test_rmq_client():
    """A simple test for the RMQ client script."""

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host="localhost",
                port=5672,
                virtual_host="/",
                credentials=pika.PlainCredentials(
                    os.environ.get("RMQ_USERNAME"), os.environ.get("RMQ_PASSWORD")
                ),
            )
        )

        channel = connection.channel()

        # Create an exchange if it doesn't exist
        rmq_exchange_name = "ai.exchange.direct"
        queue_name = "ai.agent-workflow-1"

        channel.exchange_declare(exchange=rmq_exchange_name, exchange_type="direct")
        channel.queue_declare(queue=queue_name, durable=True)

        channel.queue_bind(queue=queue_name, exchange=rmq_exchange_name, routing_key="")

        message = {
            "agent_id": "agent_123",
            "task": "process_data",
            "data": {
                "input": "sample data",
                "parameters": {"param1": "value1", "param2": "value2"},
            },
            "timestamp": datetime.now().isoformat(),
        }

        # Convert the message to a string for sending
        event_message = json.dumps(message)

        # Publish the message to the exchange
        channel.basic_publish(
            exchange=rmq_exchange_name, routing_key="", body=event_message
        )

        print(" [x] Sent %r" % message)
        connection.close()

        print("RMQ client script executed successfully.")

    except Exception as e:
        exception = e
        print(f"An error occurred: {e}")
