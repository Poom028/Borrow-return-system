#!/usr/bin/env python3
"""
Script to initialize equipment database with default items
Run this script once to set up the initial equipment data
"""

from mongoengine import connect
from models import Equipment
from config import Config

def init_equipment():
    """Initialize equipment database with default items"""
    
    # Connect to MongoDB
    if "uri" in Config.MONGODB_SETTINGS:
        connect(host=Config.MONGODB_SETTINGS["uri"])
    else:
        connect(
            db=Config.MONGODB_SETTINGS["db"],
            host=Config.MONGODB_SETTINGS["host"],
            port=Config.MONGODB_SETTINGS["port"]
        )
    
    # Default equipment items (10 items, each with quantity 10)
    default_equipment = [
        {"name": "ลูกฟุตบอล", "quantity": 10},
        {"name": "ลูกบาส", "quantity": 10},
        {"name": "ลูกตะกร้อ", "quantity": 10},
        {"name": "ลูกแบดมินตัน", "quantity": 10},
        {"name": "ลูกเบสบอล", "quantity": 10},
        {"name": "ลูกกอล์ฟ", "quantity": 10},
        {"name": "ลูกเทนนิส", "quantity": 10},
        {"name": "ลูกปิงปอง", "quantity": 10},
        {"name": "ลูกฟุตซอล", "quantity": 10},
        {"name": "ลูกวอลเล่บอล", "quantity": 10},
    ]
    
    print("Initializing equipment database...")
    
    for item in default_equipment:
        # Check if equipment already exists
        existing = Equipment.objects(name=item["name"]).first()
        if existing:
            print(f"Equipment '{item['name']}' already exists, updating quantity...")
            existing.quantity = item["quantity"]
            existing.save()
        else:
            print(f"Creating new equipment: {item['name']} (quantity: {item['quantity']})")
            equipment = Equipment(name=item["name"], quantity=item["quantity"])
            equipment.save()
    
    print("Equipment database initialization completed!")

if __name__ == "__main__":
    init_equipment()
