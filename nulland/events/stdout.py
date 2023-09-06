class Producer:
    def produce(self, topic, key, value):
        print(f"event log: topic={topic} key={key} value={value}")
