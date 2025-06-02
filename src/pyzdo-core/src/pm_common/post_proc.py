from .root_cmd import RootCmd
from .publish_to_topic_cmd import PublishToTopicCmd
from .cmd_types import CmdTypes
from .cmd_categories import CmdCategories
from .http_clients.cosmos_manager import CosmosContainerManager, CosmosQry
from .utils.env_var_provider import EnvVarProvider
from json import dumps as json_dumps
import logging

logging.basicConfig(level=logging.DEBUG)

env_var_provider = EnvVarProvider()
STORE_QUERY_URL = env_var_provider.get_env_var(
    "STORE_QUERY_URL", "http://localhost:8000/cb/qry"
)
cosmos_container_manager = CosmosContainerManager()


def enrich_payload(payload: dict, cmd: RootCmd) -> None:
    add_map = cmd._cmd_post_op_enrichement_map_()
    for m in add_map:
        payload[m["key"]] = m["val"]
    id = payload.get("id", None)
    if id:
        payload["partitionKey"] = str(id)
        payload["id"] = str(id)


def build_publish_to_topic_cmd(cmd: RootCmd, topic: str) -> PublishToTopicCmd:
    key = str(cmd.cmd_data.get("id", 0))
    cmd = PublishToTopicCmd(
        topic=topic,
        key=key,
        payload=cmd._to_dict_(),
    )

    return cmd


def build_bulk_publish_to_topic_cmd(cmd: RootCmd, topic: str) -> PublishToTopicCmd:
    key = "0"
    cmd = PublishToTopicCmd(
        topic=topic,
        key=key,
        payload=cmd._to_dict_(),
    )

    return cmd


def build_persist_cmd(payload: dict, cmd: RootCmd) -> RootCmd:
    cmd = RootCmd(
        cmd_category=CmdCategories.PERSIST.value,
        cmd_type=CmdTypes.PERSIST_TO_STORE.value,
        cmd_data=payload,
        cmd_metadata=cmd.cmd_metadata,
    )

    return cmd


def update_proc_status(status: str, cmd: RootCmd):
    batch = cmd.cmd_metadata.get("batch", "1/1")
    batch_no, batches = batch.split("/")
    container_name = "process_definitions"

    if batch_no != batches:
        return

    idempotency_id = cmd._idempotency_id_()

    try:
        cosmos_container_manager.partial_update(container_name, idempotency_id, {}, {"status": status})
    except:
        logging.error(f"Error updating process status: container name: {container_name}, idempotency id: {idempotency_id}")