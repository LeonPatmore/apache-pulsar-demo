import logging

import pulsar
import pytest

from utils import TestClient

logging.root.setLevel(logging.INFO)


@pytest.fixture(scope="session")
def client(request):
    client = pulsar.Client('pulsar://localhost:6650')
    request.addfinalizer(lambda: client.close())
    return TestClient(client)


def test_shared_subscription(client):
    consumer = client.generate_consumer()

    client.generate_n_messages(10, consumer.topic())

    client.for_n_messages(consumer, 10, lambda msg: consumer.acknowledge(msg))

    assert client.number_of_messages_for_consumer(consumer) == 0


def test_shared_subscription_when_not_acked_re_consumes_messages(client):
    topic = client.random_name()
    subscription = client.random_name()
    consumer = client.generate_consumer(topic=topic, subscription=subscription)

    client.generate_n_messages(10, topic)
    client.consume_n_messages_and_do_not_ack(consumer, 10)
    consumer.close()

    second_consumer = client.generate_consumer(topic=topic, subscription=subscription)
    assert 10 == client.number_of_messages_for_consumer(second_consumer)
