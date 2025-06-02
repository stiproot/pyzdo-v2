from algos.build_risk_weighted_work_item_tree_alpha import (
    build_risk_weighted_work_item_tree,
)
from queries import (
    get_wi_collection_hash_for_project,
    get_wi_root_collection_from_collection_hash,
)
from persists import persist_payload
from pyzdo_core import RootCmd, enrich_payload
import logging


def build_weighted_work_item_tree_workflow(cmd: RootCmd) -> int:
    collection_hash = get_wi_collection_hash_for_project(cmd)
    root_collection_name = get_wi_root_collection_from_collection_hash(collection_hash)
    root_node_ids = [
        item["id"] for item in collection_hash[root_collection_name].values()
    ]
    get_raw_node_fn = lambda id, node_type: collection_hash.get(node_type, {}).get(
        str(id), {}
    )

    structured_nodes = []
    for node_id in root_node_ids:
        structure = build_risk_weighted_work_item_tree(
            node_id, root_collection_name, get_raw_node_fn
        )
        structured_nodes.append(structure)

    tree = {"type": "root", "children": structured_nodes}
    enrich_payload(tree, cmd)

    logging.info("Finished building weighted tree.")

    persist_payload(
        payload=tree,
        cmd=cmd,
    )
