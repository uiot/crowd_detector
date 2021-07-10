import json
from kafka import KafkaConsumer

# TODO: change to host ip
kafka_broker = "localhost:9093"
topic_name = f"rules"

consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)
for msg in consumer:
    print(f"Received message: {msg}")
    # Load rule as json
    rules = json.loads(msg.value)
    # for r in rules:
      # do something