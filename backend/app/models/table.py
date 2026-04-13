from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class TableStatus(str, Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False, index=True)
    qr_token = Column(String(64), unique=True, nullable=False, index=True)
    status = Column(
        SQLEnum(TableStatus, name="table_status"),
        nullable=False,
        default=TableStatus.AVAILABLE,
    )
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False, index=True)

    restaurant = relationship("Restaurant", back_populates="tables")
    orders = relationship("Order", back_populates="table")
