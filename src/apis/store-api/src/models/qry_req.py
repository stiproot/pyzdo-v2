from pydantic import BaseModel


class QryReq(BaseModel):
    qry_data: dict