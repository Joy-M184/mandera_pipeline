""" Generate synthetic order records."""
import random
from datetime import datetime, timezone
from faker import Faker
from config.settings import CUSTOMERS_MIN, CUSTOMERS_MAX, PAYMENT_STATUSES, REGIONS, ORDERS_MIN, ORDERS_MAX, PRODUCT_IDS


fake = Faker()

def generate(batch_id: str) -> list[dict]:
    """Generate 10-20 synthetic order records with realistic data."""

    count=random.randint(ORDERS_MIN, ORDERS_MAX)
    orders = []

    for _ in range(count):
        orders.append({
            "order_id": f"ORD{random.randint(10000, 99999)}",
            "customer_id": f"CUST{random.randint(10000, 99999)}",
            "product_id": random.choice(PRODUCT_IDS),
            "region": random.choice(REGIONS),
            "mount": random.randint(1000, 50000),
            "payment_status": random.choice(PAYMENT_STATUSES),
            "batch_id": batch_id,
            "created_at": datetime.now(timezone.utc),
        })
    return orders

  
 
   

