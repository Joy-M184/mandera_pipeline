"""
 Centralized configuration for the MANDERA_PIPELINE.
 All modules import from here no hardcoded connection strings.
 """
import os
from datetime import datetime, timezone

#  MongoDB Atlas

MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise EnvironmentError("MONGO_URL is not set.Provide your MongoDB Atlas connection strings in .env")
MONGO_DB = os.getenv("MONGO_DB")


MONGO_COLLECTIONS = { 
    "customers": "customers",
    "products": "products",
    "orders": "orders",
}


# -- Source genereation settings (used by generator/) -------
ORDERS_MIN = 2000
ORDERS_MAX = 5000
CUSTOMERS_MIN = 10
CUSTOMERS_MAX = 20
PRODUCTS_MIN = 5
PRODUCTS_MAX = 10



PAYMENT_METHODS = ["Credit Card", "PayPal", "Bank Transfer", "Klarna", "Apple Pay", "Google Pay"]


PAYMENT_STATUSES = ["Pending", "Completed", "Failed", "PAID","DECLINED"]

PRODUCT_CATEGORIES = {
    "Electronics" :[
            "Smartphone", "Laptop", "Headphones", "Camera", "Smartwatch",
            "Tablet", "Earbuds", "Screen Protector", "Portable Charger"
    ],

    "Clothing": [
        "T-shirt", "DenimJ eans", "WinterJacket", "Runing Sneakers", "Shirts Dress", "Polo Hat", "Socks", 
        "Female Scarf", "Gloves", "Faux leather Belt",
   ],

    "Home & Kitchen":[
        "Smart Blender", "Water Dispenser","Non Stick Pot","Cordless Kettle", 
        "Cookware Set", "Vacuum Cleaner", "Air Fryer","Dish WAsher", "Robot Vacuum", 
        "Espresso Machine"
    ],

    "Groceries": [
        "Oats 500g", "Corn Flakes 900g", "Semi-Skimmed Milk", "Organic Apple Juice 500ml", 
        "Pited Dates 250g", "Almond Butter 300g", "Whole Wheat Bread", "Free Range Eggs 12 pack",
        "Olive Oil 1L", "Natural Peanut Butter 500g"
    ],
}

NUMBER_OF_BATCHES = int(os.getenv("NUMBER_OF_BATCHES"))
#scheduled run hour (UTC) -must mat.github/workflows/generate_data.yml cron
BATCH_SCHEDULED_HOURS = (7,15) # 7am and 3pm UTC

def generate_batch_id() -> str:

    """Auto-generate batch_id:2026_05_09_07_batch_01

    Determine the batch number based on which schedule hour 
    slot the current time falls closest to. 
    Falls back to sequential numbering if the hour doesnt match a known schedule.
    """
    
    now = datetime.now(timezone.utc)
    date_part = now.strftime("%Y_%m_%d")
    hour = now.hour

    # Determine batch number based on schedule
    batch_num = 1
    for i, scheduled_hour in enumerate(BATCH_SCHEDULED_HOURS):
        if abs(hour - scheduled_hour) <= 1:  # Within 1 hour of scheduled time
            batch_num = 1+1
            break
    else:
        #manual run outside scheduled hours_assign based on      AM/PM   
        batch_num = 1 if hour < 12 else 2
    return f"{date_part}_{hour:02d}_batch_0{batch_num}" 


REGIONS = ["North", "South", "East", "West", "Central"]

PRODUCT_IDS = [f"PROD{i:05d}" for i in range(1, 101)]
