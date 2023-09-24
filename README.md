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
