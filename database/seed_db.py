import json
import os
from sqlalchemy.orm import Session
from app_models import User, Item, Order
from database import SessionLocal
from passlib.context import CryptContext
from orders.schemas import OrderCreate, OrderItemCreate
from orders.routes.order import create_order

# For password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    # Create a database session
    db = SessionLocal()
    
    # Load data from JSON file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "seed_data.json")
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Check if we already have data (to prevent duplication)
    if db.query(User).first():
        print("Database already contains data. Skipping seed operation.")
        db.close()
        return
    
    print("Seeding users...")
    for user_data in data["users"]:

        db_user = User(
            email = user_data.get("email", ""),
            user_name = user_data.get("user_name", ""),
            full_name = user_data.get("full_name", ""),
            hashed_password = pwd_context.hash(user_data.get("password", "")),
        )

        db.add(db_user)
    db.commit()
    
    print("Seeding items...")
    for item_data in data["items"]:
        db_item = Item(**item_data)
        db.add(db_item)
    db.commit()
    

    print("Seeding orders...")
    # used create_order function to handle order creation as it is more complex
    for order_data in data["orders"]:
        order_items = []

        for item in order_data.get("items", []):
            order_items.append(OrderItemCreate(
                item_id = item.get("item_id", 0),  # Ensure item_id is present
                quantity = item.get("quantity", 1)  # Default to 1 or adjust if your seed data includes quantities
            ))

        order_create = OrderCreate(
            user_id = order_data.get("user_id", 1),
            items = order_items
        )

        create_order(order = order_create, db = db)
    
    print("Database seeded successfully!")
    db.close()

if __name__ == "__main__":
    seed_database()