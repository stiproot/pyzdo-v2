from fastapi import APIRouter
from pyzdo_core.http_clients.cosmos_manager import CosmosContainerManager, CosmosQry
from models.qry_req import QryReq
import logging

logging.basicConfig(level=logging.DEBUG)
router = APIRouter()
container_manager = CosmosContainerManager()


@router.post("/qry")
async def query(req: QryReq):
    logging.info("Query received...")

    container_name = req.qry_data["collection_name"]
    ql = req.qry_data["ql"]
    params = req.qry_data["params"]
    qry = CosmosQry(container_name, ql, params)

    try:
        rows = container_manager.process_qry(qry)
        return {"result": rows}

    except Exception as e:
        logging.error(e)
        return {"error": e, "result": []}
