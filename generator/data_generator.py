"""Orchestrates synthetic data generation -> MONGODB Atlas.
Calls each faker module and inserts generated data into MongoDB, and logs what was generated.
Designed to be called by GitHub Actions on a schedule.
"""
import json
import io
from pymongo import MongoClient
from minio import Minio
from config.settings import MONGO_URL, MONGO_DB, MONGO_COLLECTIONS, generate_batch_id
from generator import fake_customers, fake_products, fake_orders

def save_to_minio(data, filename):
    try:
        client = Minio("localhost:9000", access_key="minioadmin", secret_key="minioadmin", secure=False)
        json_bytes = json.dumps(data, default=str).encode("utf-8")
        client.put_object("mandera-pipeline", filename, io.BytesIO(json_bytes), length=len(json_bytes), content_type="application/json")
        print(f"Backed up {filename} to MinIO")
    except Exception as e:
        print(f"MinIO backup failed (non-critical): {e}")

def main():
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    batch_id = generate_batch_id()
    print(f"Using batch ID: {batch_id}")
    try:
        customers = fake_customers.generate(batch_id)
        save_to_minio(customers, f"customers/{batch_id}.json")
        db[MONGO_COLLECTIONS["customers"]].insert_many(customers)
        print(f"Inserted {len(customers)} customers into MongoDB.")
        products = fake_products.generate(batch_id)
        save_to_minio(products, f"products/{batch_id}.json")
        db[MONGO_COLLECTIONS["products"]].insert_many(products)
        print(f"Inserted {len(products)} products into MongoDB.")
        orders = fake_orders.generate(batch_id)
        save_to_minio(orders, f"orders/{batch_id}.json")
        db[MONGO_COLLECTIONS["orders"]].insert_many(orders)
        print(f"Inserted {len(orders)} orders into MongoDB.")
    finally:
        client.close()
    print("\nData generation complete.")

if __name__ == "__main__":
    main()
