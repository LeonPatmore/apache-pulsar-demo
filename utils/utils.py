import pulsar

client = pulsar.Client('pulsar://localhost:6650')

producer = client.create_producer('my-topic')

consumer = client.subscribe('my-topic', 'my-subscription', )


for i in range(10):
    producer.send(('Hello-%d' % i).encode('utf-8'))

while True:
    msg = consumer.receive()
    try:
        print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except Exception:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()
