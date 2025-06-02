from fastapi import APIRouter
from pyzdo_core.kafka.kafka_producer_manager import KafkaProducerManager
from models.publish_req import PublishReq
from json import dumps as json_dumps
import logging

logging.basicConfig(level=logging.DEBUG)

router = APIRouter()


@router.post("/topic/publish")
async def publish_to_topic(req: PublishReq):
    logging.info("Publish request received.")
    manager = KafkaProducerManager(req.topic)
    json_payload = json_dumps(req.payload)
    manager.produce(req.key, json_payload)
    manager.flush()

    return {"status": "accepted"}
