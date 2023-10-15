import logging

import pulsar
import pytest

from utils import PulsarTestClient


@pytest.fixture(scope="session")
def k8s_client(request):
    client = pulsar.Client(f"pulsar://pulsar-mini-broker-0.pulsar-mini-broker.pulsar.svc.cluster.local:6650")
    request.addfinalizer(lambda: client.close())
    return PulsarTestClient(client)


def test_function(k8s_client):
    k8s_client.generate_n_messages(1, "persistent://public/functions/inTopic")

    output_consumer = k8s_client.generate_consumer("persistent://public/functions/outTopic")

    def ack_and_log_value(msg):
        output_consumer.acknowledge(msg)
        number = int(msg.data().decode("utf-8"))
        logging.info("Received number " + str(number))
        assert number == 2

    k8s_client.for_n_messages(output_consumer, 1, ack_and_log_value)


if __name__ == '__main__':
    pytest.main([__file__])
