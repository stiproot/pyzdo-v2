from multiprocessing import JoinableQueue, Process
from gather_project_units_of_work_workflow import (
    gather_project_units_of_work_workflow,
)
from pyzdo_core import (
    CmdTypes,
    KafkaConsumerRootCmdProvider,
    EnvVarProvider,
)
import time

env_var_provider = EnvVarProvider()

WORKER_TOPIC = env_var_provider.get_env_var(
    "WORKER_TOPIC", "pyzdo_CMD_GATHER"
)
DEBUGGING = env_var_provider.get_env_var("DEBUGGING", False)

workflow_hash = {
    CmdTypes.GATHER_PROJECT_UNITS_OF_WORK: gather_project_units_of_work_workflow,
}


def queue_cmds(queue: JoinableQueue) -> None:
    cmd_provider = KafkaConsumerRootCmdProvider(topic=WORKER_TOPIC)

    while True:
        cmds = cmd_provider.provide()
        if cmds is None:
            break
        for cmd in cmds:
            queue.put(cmd)


def process_cmds(queue: JoinableQueue):
    while True:
        msg = queue.get()

        if msg is None:
            break

        workflow_hash[msg.cmd_type](msg)

        queue.task_done()


def main():
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
