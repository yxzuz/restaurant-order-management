from pydantic import BaseModel, ConfigDict
from pydantic import Field

from app.models.table import TableStatus


class TableRead(BaseModel):
    id: int
    number: int
    status: TableStatus

    model_config = ConfigDict(from_attributes=True)


class TableAccessRead(TableRead):
    qr_token: str


class TableCreate(BaseModel):
    number: int = Field(..., ge=1)


class TableAccess(BaseModel):
    table_number: int
    qr_token: str
