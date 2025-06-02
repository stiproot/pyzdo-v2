from pydantic import BaseModel
from typing import Optional

class CmdReq(BaseModel):
    cmd_data: dict
    cmd_metadata: dict


class BulkCmdReq(BaseModel):
    cmd_data: list[CmdReq]
    cmd_metadata: dict
