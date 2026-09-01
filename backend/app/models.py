from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .db import Base

class Product(Base):
    __tablename__="products"
    id: Mapped[int]=mapped_column(primary_key=True)
    sku: Mapped[str]=mapped_column(String(40), unique=True, index=True)
    name: Mapped[str]=mapped_column(String(160))
    category: Mapped[str]=mapped_column(String(80), default="General")
    price: Mapped[float]=mapped_column(Float)
    stock: Mapped[int]=mapped_column(Integer, default=0)
    reorder_level: Mapped[int]=mapped_column(Integer, default=5)

class Sale(Base):
    __tablename__="sales"
    id: Mapped[int]=mapped_column(primary_key=True)
    total: Mapped[float]=mapped_column(Float)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    items: Mapped[list["SaleItem"]]=relationship(cascade="all, delete-orphan")

class SaleItem(Base):
    __tablename__="sale_items"
    id: Mapped[int]=mapped_column(primary_key=True)
    sale_id: Mapped[int]=mapped_column(ForeignKey("sales.id"))
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]=mapped_column(Integer)
    unit_price: Mapped[float]=mapped_column(Float)
