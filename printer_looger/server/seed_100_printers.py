"""Seed 100 active printers per department into MongoDB."""

"""try:
    from pymongo import MongoClient  # type: ignore[import]
    from pymongo.database import Database  # type: ignore[import]
    from pymongo.collection import Collection  # type: ignore[import]
except ImportError:
    print("Error: pymongo is not installed. Install it with: pip install pymongo")
    exit(1)

import os
from typing import Any

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client: Any = MongoClient(MONGO_URI)
db: Any = client["printer_project"]
collection: Any = db["printers"]

departments = [
    "Knitting",
    "Legal",
    "IT",
    "Mechanic",
    "Technician",
    "Guardian",
    "Security",
    "HR",
    "Finance",
    "Admin",
]
model_prefix = {
    "Knitting": "RICOH MP",
    "Legal": "HP LaserJet M",
    "IT": "RICOH IM C",
    "Mechanic": "Brother HL-L",
    "Technician": "Xerox VersaLink C",
    "Guardian": "Canon imageRUNNER",
    "Security": "Lexmark MS",
    "HR": "Epson WorkForce",
    "Finance": "Dell B",
    "Admin": "Samsung ProXpress",
}

printers = []
for dept_idx, dept in enumerate(departments):
    for i in range(1, 101):
        printers.append(
            {
                "printer_name": f"{dept}_Printer_{i}",
                "department": dept,
                "level": f"Level {(i % 3) + 1}",
                "model_number": f"{model_prefix[dept]} {4000 + i}",
                "ip_address": f"192.168.{dept_idx + 1}.{i}",
                "is_active": True,
            }
        )

if collection.count_documents({}) == 0:
    collection.insert_many(printers)
    print(f"Inserted {len(printers)} printers.")
else:
    print("Printers already exist. Skipping seed.")"""
