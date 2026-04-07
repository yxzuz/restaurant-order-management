from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class TableStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, nullable=False, index=True)
    qr_token = Column(String(64), unique=True, nullable=False, index=True)
    status = Column(
        SQLEnum(TableStatus, name="table_status"),
        nullable=False,
        default=TableStatus.AVAILABLE,
    )

    orders = relationship("Order", back_populates="table")
