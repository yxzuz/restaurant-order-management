from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Integer
from sqlalchemy.orm import relationship
from app.db import Base


class OrderStatus(str, Enum):
    NEW = "new"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(
        SQLEnum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.NEW,
    )
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    items = relationship("OrderItem", back_populates="order")
