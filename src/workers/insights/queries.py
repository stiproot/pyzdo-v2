from json import dumps as json_dumps
from json import loads as json_loads
from pm_common import RootCmd, CosmosContainerManager, CosmosQry
import logging

logging.basicConfig(level=logging.DEBUG)

cosmos_container_manager = CosmosContainerManager()


COLLECTIONS = [
    "programmes",
    "large_projects",
    "medium_projects",
    "initiatives",
    "epics",
    "features",
    "user_stories",
    "tasks",
    "bugs",
    "impediments"
]

WORK_ITEM_TYPE_COLLECTION_HASH = {
    "Programme": "programmes",
    "Large Project": "large_projects",
    "Medium Project": "medium_projects",
    "Initiative": "initiatives",
    "Epic": "epics",
    "Feature": "features",
    "User Story": "user_stories",
    "Task": "tasks",
    "Bug": "bugs",
    "Impediment": "impediments"
}


def get_wi_collection_hash_for_project(cmd: RootCmd) -> str:
    project_id = cmd.cmd_metadata["project_id"]
    collection_hash = {}

    for c in COLLECTIONS:
        ql = f"SELECT * FROM c WHERE c.__metadata__.project_id = '{project_id}'"
        logging.debug(f"ql: {ql}")

        qry = CosmosQry(c, ql, [])

        try:
            resp = cosmos_container_manager.process_qry(qry)
            hash = {}
            for item in resp:
                hash[item["id"]] = item
            collection_hash[c] = hash
        except Exception as e:
            logging.error(f"Error collection ({c}) for project '{project_id}'")
            logging.error("Error:::", e)

    return collection_hash


def get_wi_root_collection_from_collection_hash(hash: dict) -> str:
    for c in COLLECTIONS:
        if len(hash.get(c, {})) > 0:
            return c

    raise Exception("Could not find root collection")