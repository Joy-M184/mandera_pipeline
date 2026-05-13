""" Generate synthetic product records."""
import random
from datetime import datetime, timezone
from faker import Faker
from config.settings import PRODUCTS_MAX, PRODUCTS_MIN, PRODUCTS_MAX_MAX


fake = Faker()

PRODUCT_CATEGORIES = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones", "Monitor"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Shoes", "Dress"],
    "Home": ["Lamp", "Pillow", "Blanket", "Chair", "Table"],
    "Books": ["Novel", "Science", "History", "Poetry", "Biography"],
}

def generate(batch_id: str) -> list[dict]:
    """Generate 5-10 synthetic product records with realistic data."""

    count=random.randint(PRODUCTS_MIN, PRODUCTS_MAX)
    products = []

    for _ in range(count):
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        products.append({
            "product_id": f"PROD{random.randint(10000, 99999)}",
            "product_name": random.choice(PRODUCT_CATEGORIES[category]),
            "category" : category,
            "price": round(random.uniform(50,15000), 2),
            "batch_id": batch_id,
            "created_at": datetime.now(timezone.utc),
        })
    return products

