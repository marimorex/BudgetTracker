import pika


class RabbitMQConnectionManager:
    def __init__(self, host="rabbitmq_server"):
        self.host = host
        self.port = 5672
        self.credentials = pika.PlainCredentials("guest", "guest")
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host, port=self.port, credentials=self.credentials
                )
            )
        return self.connection

    def get_channel(self):
        if not self.channel or self.channel.is_closed:
            self.channel = self.connect().channel()
        return self.channel

    def close(self):
        if self.channel and not self.channel.is_closed:
            self.channel.close()
        if self.connection and not self.connection.is_closed:
            self.connection.close()


client_manager = RabbitMQConnectionManager()
