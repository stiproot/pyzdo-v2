from multiprocessing import JoinableQueue, Process
from pyzdo_core import (
    HttpClient,
    KafkaConsumerRootCmdProvider,
    EnvVarProvider,
)
from persist_cmd_processor import PersistCmdProcessor
import time
import logging

logging.basicConfig(level=logging.DEBUG)

env_var_provider = EnvVarProvider()
WORKER_TOPIC = env_var_provider.get_env_var(
    "WORKER_TOPIC", "pyzdo_CMD_PERSIST"
)
STORE_COMMAND_URL = env_var_provider.get_env_var(
    "STORE_COMMAND_URL", "http://localhost:8000/store/cmd"
)
STORE_BULK_COMMAND_URL = env_var_provider.get_env_var(
    "STORE_BULK_COMMAND_URL", "http://localhost:8000/store/cmds"
)
DEBUGGING = env_var_provider.get_env_var("DEBUGGING", False)

print("ENVIRONMENT VARIABLES:")
print(f"WORKER_TOPIC: {WORKER_TOPIC}")
print(f"STORE_COMMAND_URL: {STORE_COMMAND_URL}")
print(f"DEBUGGING: {DEBUGGING}")


def queue_cmds(queue: JoinableQueue) -> None:
    cmd_provider = KafkaConsumerRootCmdProvider(topic=WORKER_TOPIC)

    while True:
        cmds = cmd_provider.provide()
        if cmds is None:
            break
        for cmd in cmds:
            queue.put(cmd)


def process_cmds(queue: JoinableQueue):
    http_client = HttpClient(STORE_COMMAND_URL)
    bulk_http_client = HttpClient(STORE_BULK_COMMAND_URL)
    cmd_processor = PersistCmdProcessor(
        http_client=http_client, bulk_http_client=bulk_http_client
    )

    while True:
        msg = queue.get()
        if msg is None:
            break
        cmd_processor.process(msg)
        queue.task_done()


def main():
    logging.info("Starting persist worker...")
    NUM_PROCS = 1
    queue = JoinableQueue()

    providers = []
    for _ in range(NUM_PROCS):
        provider = Process(target=queue_cmds, args=(queue,))
        providers.append(provider)
        provider.start()

    workers = []
    for _ in range(NUM_PROCS):
        worker = Process(target=process_cmds, args=(queue,))
        workers.append(worker)
        worker.start()

    # for _ in range(NUM_PROCS):
    #     queue.put(None)  # Signal workers to exit

    for provider in providers:
        provider.join()

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    if not DEBUGGING:
        time.sleep(30)
    main()
