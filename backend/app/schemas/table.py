from pydantic import BaseModel, ConfigDict

from app.models.table import TableStatus


class TableRead(BaseModel):
    id: int
    number: int
    status: TableStatus

    model_config = ConfigDict(from_attributes=True)


class TableAccess(BaseModel):
    table_number: int
    qr_token: str
