from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from .db import Base, engine, get_db
from .models import Product, Sale, SaleItem
from .schemas import ProductCreate, ProductOut, StockAdjustment, Checkout, SaleOut

app=FastAPI(title="RetailForge POS API", version="1.0.0")
Base.metadata.create_all(engine)

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/api/products", response_model=list[ProductOut])
def products(db:Session=Depends(get_db)):
    return db.query(Product).order_by(Product.name).all()

@app.post("/api/products", response_model=ProductOut, status_code=201)
def create_product(payload:ProductCreate, db:Session=Depends(get_db)):
    if db.query(Product).filter_by(sku=payload.sku).first():
        raise HTTPException(409,"SKU already exists")
    obj=Product(**payload.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

@app.patch("/api/products/{product_id}/stock", response_model=ProductOut)
def adjust_stock(product_id:int,payload:StockAdjustment,db:Session=Depends(get_db)):
    p=db.get(Product,product_id)
    if not p: raise HTTPException(404,"Product not found")
    if p.stock+payload.quantity<0: raise HTTPException(400,"Insufficient stock")
    p.stock+=payload.quantity; db.commit(); db.refresh(p); return p

@app.get("/api/dashboard")
def dashboard(db:Session=Depends(get_db)):
    revenue=db.query(func.coalesce(func.sum(Sale.total),0)).scalar()
    low=db.query(Product).filter(Product.stock<=Product.reorder_level).count()
    sales=db.query(Sale).count()
    return {"revenue":round(float(revenue),2),"sales_count":sales,"low_stock_items":low}

@app.post("/api/checkout",response_model=SaleOut,status_code=201)
def checkout(payload:Checkout,db:Session=Depends(get_db)):
    if not payload.items: raise HTTPException(400,"Cart is empty")
    total=0.0; resolved=[]
    for line in payload.items:
        p=db.get(Product,line.product_id)
        if not p: raise HTTPException(404,f"Product {line.product_id} not found")
        if p.stock<line.quantity: raise HTTPException(400,f"Insufficient stock for {p.name}")
        total+=p.price*line.quantity; resolved.append((p,line.quantity))
    sale=Sale(total=round(total,2)); db.add(sale)
    for p,q in resolved:
        p.stock-=q
        sale.items.append(SaleItem(product_id=p.id,quantity=q,unit_price=p.price))
    db.commit(); db.refresh(sale)
    return sale
