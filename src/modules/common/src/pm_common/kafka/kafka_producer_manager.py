from confluent_kafka import Producer
from pm_common.utils.env_var_provider import EnvVarProvider


class ProducerConfigurationBuilder:
    def __init__(self):
        self._env = EnvVarProvider()

    def build(self) -> dict[str, str]:
        config = {
            "bootstrap.servers": self._env.get_env_var("KAFKA_BOOTSTRAP_SERVERS"),
            "security.protocol": self._env.get_env_var("KAFKA_SECURITY_PROTOCOL"),
            "sasl.mechanisms": self._env.get_env_var("KAFKA_SASL_MECHANISMS"),
            "sasl.username": self._env.get_env_var("KAFKA_SASL_USERNAME"),
            "sasl.password": self._env.get_env_var("KAFKA_SASL_PASSWORD"),
            # "group.id": self._env.get_env_var("KAFKA_GROUP_ID"),
            # "auto.offset.reset": "earliest",
            "client.id": self._env.get_env_var("CLIENT_ID"),
        }
        print(config)
        return config


class KafkaProducerManager:
    def __init__(self, topic: str):
        self._topic = topic
        self._configuration = ProducerConfigurationBuilder().build()
        self._producer = Producer(self._configuration)

    def produce(self, key: str, value: str):
        self._producer.produce(self._topic, key=key, value=value)
        return self

    def flush(self):
        self._producer.flush()
        return self
