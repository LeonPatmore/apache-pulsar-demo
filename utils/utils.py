import logging
import time
import uuid

import pulsar
from _pulsar import ConsumerType, InitialPosition


class PulsarTestClient:

    def __init__(self, client: pulsar.Client):
        self.client = client

    def generate_n_messages(self, n: int, topic: str):
        logging.info(f"Generating [ {n} ] messages to topic [ {topic} ]")
        producer = self.client.create_producer(topic)
        for i in range(n):
            producer.send(str(i + 1).encode('utf-8'))
        logging.info(f"Generated {n} messages")

    @staticmethod
    def random_name():
        return str(uuid.uuid4())

    def generate_consumer(self,
                          topic: str or None = None,
                          subscription: str or None = None):
        topic = self.random_name() if not topic else topic
        subscription = self.random_name() if not subscription else subscription
        logging.info(f"Using topic [ {topic} ] and subscription [ {subscription} ]")
        return self.client.subscribe(topic=topic,
                                     negative_ack_redelivery_delay_ms=1000,
                                     dead_letter_policy=pulsar.ConsumerDeadLetterPolicy(
                                         max_redeliver_count=1
                                     ),
                                     subscription_name=subscription,
                                     consumer_type=ConsumerType.Shared,
                                     unacked_messages_timeout_ms=10000,
                                     initial_position=InitialPosition.Earliest)

    @staticmethod
    def number_of_messages_for_consumer(consumer: pulsar.Consumer) -> tuple:
        num_received = 0
        already_received_messages = list()
        start_time = time.time()
        while time.time() - start_time < 12.0:
            try:
                timeout = 12.0 - (time.time() - start_time)
                msg = consumer.receive(timeout_millis=int(timeout*1000))
                if msg.message_id() in already_received_messages:
                    continue
                else:
                    num_received += 1
                    already_received_messages.append(msg.message_id())
            except Exception:
                break
        return num_received, already_received_messages

    def consume_n_messages_and_do_not_ack(self, consumer: pulsar.Consumer, n: int):
        self.for_n_messages(consumer, n)

    @staticmethod
    def for_n_messages(consumer: pulsar.Consumer, n: int, do: callable = lambda *_, **__: None):
        num_received = 0
        while True:
            msg = consumer.receive(timeout_millis=12000)
            try:
                logging.info(f"Received message [ {msg.data()} ] with id [ {msg.message_id()} ]")
                do(msg)
                num_received += 1
                logging.info(f"Num received is now {num_received} / {n}")
                if num_received >= n:
                    return
            except Exception as e:
                logging.error("Failed to process message due to " + str(e))
                # Message failed to be processed
                consumer.negative_acknowledge(msg)
