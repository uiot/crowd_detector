import json
from kafka import KafkaConsumer

# TODO: change to host ip
kafka_broker = "192.168.68.121:9093"
topic_name = "rules"

print("Starting consumer...") 
consumer = KafkaConsumer(topic_name, bootstrap_servers=kafka_broker)
print("Consumer started")
for msg in consumer:
    print(f"Received message: {msg}")
    # Load rule as json
    rules = json.loads(msg.value)
    # for r in rules:
      # do something
