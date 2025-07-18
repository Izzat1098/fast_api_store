from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float, func
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="pending")
    
    # Relationships
    user = relationship("User")
    items = relationship("OrderItem", back_populates="order")
    

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    item_id = Column(Integer, ForeignKey("items.item_id"))
    quantity = Column(Integer, default=1)
    
    # Relationships
    order = relationship("Order", back_populates="items")
    item = relationship("Item")