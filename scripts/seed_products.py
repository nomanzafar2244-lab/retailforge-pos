import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
DATA_FILE = ROOT_DIR / "data" / "demo_products.json"

sys.path.insert(0, str(BACKEND_DIR))

os.chdir(BACKEND_DIR)

from app.db import Base, SessionLocal, engine
from app.models import Product


def load_products():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_products():
    Base.metadata.create_all(bind=engine)

    products = load_products()

    db = SessionLocal()

    try:
        existing_skus = {
            sku
            for (sku,) in db.query(Product.sku).all()
        }

        new_products = [
            Product(**product)
            for product in products
            if product["sku"] not in existing_skus
        ]

        if not new_products:
            print("No new products to seed.")
            print(f"{len(existing_skus)} products already exist.")
            return

        db.add_all(new_products)
        db.commit()

        print(f"Successfully seeded {len(new_products)} new products.")

    except Exception as exc:
        db.rollback()
        print(f"Seed failed: {exc}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_products()