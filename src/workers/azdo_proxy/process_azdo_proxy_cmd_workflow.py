from pm_common import (
    RootCmd,
    PublishToTopicCmdProcessor,
    KafkaHttpClient,
    CmdTypes,
    AzdoProxyHttpClient,
    EnvVarProvider,
    update_proc_status,
)


env_var_provider = EnvVarProvider()
PERSIST_TOPIC = env_var_provider.get_env_var(
    "PERSIST_TOPIC", "PROJECTM_CMD_PERSIST"
)
PERSIST_URL = env_var_provider.get_env_var(
    "PERSIST_URL", "http://localhost:8001/kafka/topic/publish"
)
AZDO_PROXY_BASE_URL = env_var_provider.get_env_var(
    "AZDO_PROXY_BASE_URL", "http://project-m-azdo-proxy-api:80"
)

persist_proc = PublishToTopicCmdProcessor(KafkaHttpClient(base_url=PERSIST_URL))
azdo_proxy_client = AzdoProxyHttpClient(base_url=AZDO_PROXY_BASE_URL)

fn_hash = {
    CmdTypes.BULK_CREATE_UNITS_OF_WORK: lambda cmd_data: azdo_proxy_client.bulkCreateWi(cmd_data),
    CmdTypes.CLONE_UNIT_OF_WORK: lambda cmd_data: azdo_proxy_client.cloneWi(cmd_data),
    CmdTypes.CREATE_DASHBOARD: lambda cmd_data: azdo_proxy_client.createDashboard(cmd_data),
    CmdTypes.UPDATE_UNIT_OF_WORK: lambda cmd_data: azdo_proxy_client.updateWi(cmd_data),
    CmdTypes.UPDATE_UNIT_OF_WORK_HIERARCHY: lambda cmd_data: azdo_proxy_client.updateWiHierarchy(cmd_data),
}


def process_azdo_proxy_cmd_workflow(cmd: RootCmd) -> int:
    cmd_type = cmd.cmd_type
    cmd_data = cmd.cmd_data

    resp = fn_hash[cmd_type](cmd_data)

    update_proc_status(status="COMPLETE", cmd=cmd)
