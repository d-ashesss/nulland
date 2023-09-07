import logging

from confluent_kafka import Producer as KafkaProducer
from nulland.config import settings


logger = logging.getLogger(__name__)


class Producer:
    def __init__(self):
        if not settings.kafka_bootstrap_servers:
            raise Exception("Kafka bootstrap servers not configured")

        cfg = {
            "client.id": settings.kafka_client_id,
            "bootstrap.servers": settings.kafka_bootstrap_servers,
        }
        if settings.kafka_sasl_username:
            cfg.update({
                "security.protocol": "SASL_SSL",
                "sasl.mechanisms": "PLAIN",
                "sasl.username": settings.kafka_sasl_username,
                "sasl.password": settings.kafka_sasl_password,
            })
        self.producer = KafkaProducer(cfg)

    def produce(self, topic, key, value):
        self.producer.produce(topic, key=key, value=value, on_delivery=self.delivery_callback)

    def delivery_callback(self, err, _):
        if err:
            logger.error(f"Kafka message delivery failed: {err}")
