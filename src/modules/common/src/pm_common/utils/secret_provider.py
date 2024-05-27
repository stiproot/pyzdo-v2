# from environs import Env
# from pm_common.utils.kv_manager import KvManager

# keys = ["COSMOS_DB_PRIMARY_KEY"]
# hash = {"COSMOS_DB_PRIMARY_KEY": "COSMOS-DB-PRIMARY-KEY"}

# class SecretProvider:
#     def __init__(self):
#         self._env = Env()
#         self._env.read_env(".env")
#         if self._env("ENVIRONMENT") == "aks":
#             self._kv_manager = KvManager()

#     def get_secret(self, secret_name: str) -> str:
#         if self._env("ENVIRONMENT") == "aks" and secret_name in keys:
#             return self._kv_manager.get_secret(hash[secret_name]) 
#         return self._env(secret_name)
