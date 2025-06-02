from azure.cosmos import CosmosClient, PartitionKey
from typing import Optional
from pyzdo_core.utils.env_var_provider import EnvVarProvider
import logging

logging.basicConfig(level=logging.DEBUG)


database_name = ""
endpoint = ""
cosmos_primary_key_name = "COSMOS_DB_PRIMARY_KEY"
cosmos_url_key_name = "COSMOS_URL"
cosmos_db_name_key_name = "COSMOS_DATABASE_NAME"


class CosmosCmd:
    container_name: str
    payload: dict

    def __init__(self, container_name, payload):
        self.container_name = container_name
        self.payload = payload


class CosmosQry:
    container_name: str
    ql: str
    params: list

    def __init__(self, container_name: str, ql: str, params: Optional[list] = []):
        self.container_name = container_name
        self.ql = ql
        self.params = params


class CosmosClientFactory:
    def __init__(self, env_var_provider: Optional[EnvVarProvider] = None):
        self._env_var_provider = env_var_provider or EnvVarProvider()

    def create_client(self) -> CosmosClient:
        key = self._env_var_provider.get_env_var(cosmos_primary_key_name)
        return CosmosClient(endpoint, key)


class CosmosContainerManager:
    def __init__(self, env_var_provider: Optional[EnvVarProvider] = None):
        self._env_var_provider = env_var_provider or EnvVarProvider()
        cosmos_db_name = self._env_var_provider.get_env_var(cosmos_db_name_key_name)
        self._db_client = CosmosClientFactory().create_client().get_database_client(cosmos_db_name)
        self._container_clients = {}
        logging.info("Cosmos container manager initialized...")

    def get_container(self, container_name):
        if container_name not in self._container_clients:
            container_client = self._db_client.get_container_client(container_name) 
            self._container_clients[container_name] = container_client
            return container_client
        else:
            return self._container_clients[container_name]

    async def upsert(self, container_name: str, json_payload: dict):
        container_client = self.get_container(container_name)
        container_client.upsert_item(body=json_payload)

    def query(self, container_name: str, ql: str, params: Optional[list] = []):
        container_client = self.get_container(container_name)
        try:
            result = container_client.query_items(ql, parameters=params, enable_cross_partition_query=True)
            return list(result)
        except Exception as e:
            logging.error(f"Error querying container {container_name}. error: {e}, ql: {ql}, params: {params}")
            return []

    def partial_update(self, container_name: str, id: str, partition_key, update_payload: dict):
        container_client = self.get_container(container_name)
        document = container_client.read_item(item=id, partition_key=partition_key)
        for k in update_payload:
            document[k] = update_payload[k]
        container_client.upsert_item(body=document)

    async def process_cmd(self, cmd: CosmosCmd):
        await self.upsert(cmd.container_name, cmd.payload)

    def process_qry(self, qry: CosmosQry):
        return self.query(qry.container_name, qry.ql, qry.params)