import logging

import pulsar
import pytest

from utils import PulsarTestClient

logging.root.setLevel(logging.INFO)


@pytest.fixture(scope="session")
def client(request):
    client = pulsar.Client('pulsar://localhost:6650')
    request.addfinalizer(lambda: client.close())
    return PulsarTestClient(client)


def test_shared_subscription(client):
    consumer = client.generate_consumer()

    client.generate_n_messages(10, consumer.topic())

    client.for_n_messages(consumer, 10, lambda msg: consumer.acknowledge(msg))

    assert client.number_of_messages_for_consumer(consumer)[0] == 0


def test_shared_subscription_when_not_acked_re_consumes_messages(client):
    topic = client.random_name()
    subscription = client.random_name()
    consumer = client.generate_consumer(topic=topic, subscription=subscription)

    client.generate_n_messages(10, topic)
    client.consume_n_messages_and_do_not_ack(consumer, 10)
    consumer.close()

    second_consumer = client.generate_consumer(topic=topic, subscription=subscription)
    assert 10 == client.number_of_messages_for_consumer(second_consumer)[0]


def test_only_non_acked_messages_are_re_consumed(client):
    topic = client.random_name()
    subscription = client.random_name()
    consumer = client.generate_consumer(topic=topic, subscription=subscription)

    def ack_if_below_6(msg):
        msg_number = int(msg.data().decode())
        if msg_number < 6:
            consumer.acknowledge(msg)

    client.generate_n_messages(10, topic)

    client.for_n_messages(consumer, 10, ack_if_below_6)

    consumer.close()

    second_consumer = client.generate_consumer(topic=topic, subscription=subscription)
    assert 5 == client.number_of_messages_for_consumer(second_consumer)[0]


def test_negative_acked_messages_are_re_consumed(client):
    topic = client.random_name()
    subscription = client.random_name()
    consumer = client.generate_consumer(topic=topic, subscription=subscription)

    def ack_if_below_6(msg):
        msg_number = int(msg.data().decode())
        if msg_number < 6:
            consumer.negative_acknowledge(msg)
        else:
            consumer.acknowledge(msg)

    client.generate_n_messages(10, topic)

    client.for_n_messages(consumer, 10, ack_if_below_6)

    consumer.close()

    second_consumer = client.generate_consumer(topic=topic, subscription=subscription)
    assert 5 == client.number_of_messages_for_consumer(second_consumer)[0]


def test_dlq_with_negative_acked(client):
    consumer = client.generate_consumer()

    client.generate_n_messages(1, consumer.topic())

    client.for_n_messages(consumer, 1, lambda msg: consumer.negative_acknowledge(msg))

    client.for_n_messages(consumer, 1, lambda msg: consumer.negative_acknowledge(msg))

    assert 0 == client.number_of_messages_for_consumer(consumer)[0]

    dlq_consumer = client.generate_consumer(topic=consumer.topic() + "-" + consumer.subscription_name() + "-DLQ")
    assert 1 == client.number_of_messages_for_consumer(dlq_consumer)[0]


def test_dlq_with_ack_timeout(client):
    consumer = client.generate_consumer()

    client.generate_n_messages(1, consumer.topic())

    client.for_n_messages(consumer, 1)

    client.for_n_messages(consumer, 1)

    assert 0 == client.number_of_messages_for_consumer(consumer)[0]

    dlq_consumer = client.generate_consumer(topic=consumer.topic() + "-" + consumer.subscription_name() + "-DLQ")
    assert 1 == client.number_of_messages_for_consumer(dlq_consumer)[0]
