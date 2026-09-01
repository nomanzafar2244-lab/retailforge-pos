from pydantic import BaseModel, Field
class ProductCreate(BaseModel):
    sku:str
    name:str
    category:str="General"
    price:float=Field(gt=0)
    stock:int=Field(ge=0)
    reorder_level:int=Field(default=5,ge=0)
class ProductOut(ProductCreate):
    id:int
    model_config={"from_attributes":True}
class StockAdjustment(BaseModel):
    quantity:int
class SaleLine(BaseModel):
    product_id:int
    quantity:int=Field(gt=0)
class Checkout(BaseModel):
    items:list[SaleLine]
class SaleOut(BaseModel):
    id:int
    total:float
