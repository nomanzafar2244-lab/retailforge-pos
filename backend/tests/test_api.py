from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health(): assert client.get("/health").json()["status"]=="ok"

def test_product_and_checkout():
    sku="TEST-"+__import__("uuid").uuid4().hex[:8]
    r=client.post("/api/products",json={"sku":sku,"name":"Demo Milk","price":3.5,"stock":10,"reorder_level":2})
    assert r.status_code==201
    pid=r.json()["id"]
    r=client.post("/api/checkout",json={"items":[{"product_id":pid,"quantity":2}]})
    assert r.status_code==201 and r.json()["total"]==7.0
