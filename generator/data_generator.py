"""Orchestrates synthetic data generation -> MONGODB Atlas.
Calls each faker module and inserts generated data into MongoDB, and logs what was generated.Designed to be called by GitHub Actions on a schedule.

Usage:
    python  -m generator. data_generator
"""

from pymongo import MongoClient

from config.settings import MONGO_URL, MONGO_DB, MONGO_COLLECTIONS, generate_batch_id
from generator import fake_customers, fake_products, fake_orders

def main():
    """Main function to generate and insert synthetic data into MongoDB."""
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB]

    # Generate batch_id once so all records in this run share the same batch_id
    batch_id = generate_batch_id()
    print(f"Using batch ID: {batch_id}")

    try:

        # Generate and insert customers
        customers = fake_customers.generate(batch_id)
        db[MONGO_COLLECTIONS['customers']].insert_many(customers)
        print(f"Inserted {len(customers)} customers into MongoDB.")
    
        # Generate and insert products
        products = fake_products.generate(batch_id)
        db[MONGO_COLLECTIONS['products']].insert_many(products)
        print(f"Inserted {len(products)} products into MongoDB.")

        #Get all customer/product IDS so orders references the full pool
        #all_customer_ids = db[MONGO_COLLECTIONS["customers"]].distinct ("customer_id")
        #all_product_ids = db[MONGO_COLLECTIONS["products"]].distinct ("product_id")

        # Generate and insert orders
        orders = fake_orders.generate(batch_id)
        db[MONGO_COLLECTIONS['orders']].insert_many(orders)
        print(f"Inserted  {len(orders)} orders into MongoDB.")
        
    finally:
        client.close()
    print("\nData generation complete.")    
        
if __name__ == "__main__":
    main()
