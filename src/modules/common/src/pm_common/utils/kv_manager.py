# from azure.identity import DefaultAzureCredential, EnvironmentCredential
from azure.identity import EnvironmentCredential
from azure.keyvault.secrets import SecretClient
import logging

logging.basicConfig(level=logging.DEBUG)

KEY_VAULT_URL = ""


class KvManager:
    def __init__(self):
        # credential = DefaultAzureCredential()
        logging.info("Attempting to invoke env. credential.")
        credential = EnvironmentCredential()
        self._secret_client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
        logging.info("Secret client initialized.")

    def get_secret(self, secret_name: str) -> str:
        retrieved_secret = self._secret_client.get_secret(secret_name)
        return retrieved_secret.value