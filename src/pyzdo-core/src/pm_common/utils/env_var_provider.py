from environs import Env
from typing import Optional
from pyzdo_core.utils.kv_manager import KvManager

keys = ["COSMOS_DB_PRIMARY_KEY", "KAFKA_SASL_USERNAME", "KAFKA_SASL_PASSWORD"]
hash = {
    "COSMOS_DB_PRIMARY_KEY": "COSMOS-DB-PRIMARY-KEY",
    "KAFKA_SASL_USERNAME": "KAFKA-API-KEY",
    "KAFKA_SASL_PASSWORD": "KAFKA-API-SECRET"
}

class EnvVarProvider:
    def __init__(self):
        self._env = Env()
        self._env.read_env(".env")
        if self._env("ENVIRONMENT") == "aks":
            self._kv_manager = KvManager()

    def get_env_var(self, key: str, default: Optional[str] = "") -> str:
        if self._env("ENVIRONMENT") == "aks" and key in keys:
            return self._kv_manager.get_secret(hash[key]) 

        val = self._env(key)
        if val is None or val == "":
            return default
        return val
