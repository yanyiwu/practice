from kafka import KafkaProducer
from kafka.errors import KafkaError
import msgpack
import json

producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), 
                         bootstrap_servers=['127.0.0.1:9092'])
future = producer.send('json-topic', {'key': 'value'})
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass
producer.flush()
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)

exit(1)


producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])

# Asynchronous by default
future = producer.send('my-topic', b'raw_bytes')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)

# produce keyed messages to enable hashed partitioning
producer.send('my-topic', key=b'foo', value=b'bar')

# encode objects via msgpack
producer = KafkaProducer(value_serializer=msgpack.dumps)
producer.send('msgpack-topic', {'key': 'value'})

# produce json messages
producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'), 
                         bootstrap_servers=['127.0.0.1:9092'])
producer.send('json-topic', {'key': 'value'})

# produce asynchronously
for _ in range(100):
    producer.send('json-topic', b'msg')

print "block until all async messages are sent"
producer.flush()

# configure multiple retries
producer = KafkaProducer(retries=5)
