# Pulsar

## Message Attributes

- Value
- Key: Useful for Topic Compaction.
- Properties: A key-value map of user defined properties.
- Producer name
- Topic name
- Schema version: Version number of the message schema.
- Sequence ID: Each message belongs to an ordered sequence on its topic. Can be used for message deduplication.
- Message ID: Assigned by bookies when the message is persisted.
- Publish time: Timestamp when the message is published.
- Event time: Optional timestmap set by the applications.

## Namespace

A namespace is a collection of topics.
One way to use namespaces is to create a namespace per application, and then the application can safely manage its own topics.

## Subscriptions

A named configuration that controls how messages are delivered to consumers. There are 4 types:

- `Exclusive`: Only one consumer can use this subscription.
- `Failover`: Multiple consumers can connect, but one is determined to be master and the others are failover.
- `Shared`: Multiple consumers consume at the same time (round robin).
- `Key Shared`: Multiple consumers can consume at the same time, but messages with the same key always go to the same consumer.
