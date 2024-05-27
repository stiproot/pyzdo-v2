from fastapi import APIRouter
from pm_common.http_clients.cosmos_manager import CosmosContainerManager, CosmosCmd
from models.cmd_req import CmdReq, BulkCmdReq
import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()
container_manager = CosmosContainerManager()

def get_container_name(cmd_req: CmdReq):
    cmd_post_op_metadata = cmd_req.cmd_metadata["cmd_post_op"]
    store_metadata = cmd_post_op_metadata["store"]
    container_name = store_metadata.get("trgt_collection", None)
    if container_name is None:
        raise Exception("Container name not found in metadata of store CmdReq!")
    return container_name


@router.post("/cmd")
async def command(req: CmdReq):
    logging.info("Command received...")

    container_name = get_container_name(req)
    data = req.cmd_data

    if not isinstance(data, list):
        logging.debug("cmd_data is not a list...")
        cmd = CosmosCmd(container_name, data)
        await container_manager.process_cmd(cmd)
        return {"status": "accepted"}

    for d in data:
        cmd = CosmosCmd(container_name, d)
        await container_manager.process_cmd(cmd)
    return {"status": "accepted"}


@router.post("/cmds")
async def command(req: BulkCmdReq):
    logging.info("Bulk command received...")

    for cmd_req in req.cmd_data:
        container_name = get_container_name(cmd_req)
        data = cmd_req.cmd_data
        cmd = CosmosCmd(container_name, data)
        await container_manager.process_cmd(cmd)

    return {"status": "accepted"}
