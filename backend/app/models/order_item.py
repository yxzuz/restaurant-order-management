from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

from app.db import Base
from app.core.timezone import now_thai


class ItemStatus(str, Enum):
    NEW = "NEW"
    PREPARING = "PREPARING"
    READY = "READY"
    COMPLETED = "COMPLETED"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"),
                      nullable=False, index=True)
    menu_item_id = Column(Integer, ForeignKey(
        "menu_items.id", ondelete="SET NULL"), nullable=True, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    status = Column(
        SQLEnum(ItemStatus, name="item_status"),
        nullable=False,
        default=ItemStatus.NEW,
    )
    created_at = Column(DateTime, nullable=False, default=now_thai)
    updated_at = Column(DateTime, nullable=False,
                        default=now_thai, onupdate=now_thai)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")
