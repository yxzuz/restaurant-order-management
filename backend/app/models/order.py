from enum import Enum

from datetime import datetime

from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db import Base
from app.core.timezone import now_thai


class OrderStatus(str, Enum):
    NEW = "new"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    UNPAID = "unpaid"
    PAID = "paid"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"),
                      nullable=False, index=True)
    restaurant_id = Column(Integer, ForeignKey(
        "restaurants.id"), nullable=False, index=True)
    status = Column(
        SQLEnum(OrderStatus, name="order_status"),
        nullable=False,
        default=OrderStatus.NEW,
    )
    payment_status = Column(
        SQLEnum(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.UNPAID,
    )
    created_at = Column(DateTime, nullable=False, default=now_thai)
    updated_at = Column(DateTime, nullable=False,
                        default=now_thai, onupdate=now_thai)
    closed_at = Column(DateTime)

    restaurant = relationship("Restaurant", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
