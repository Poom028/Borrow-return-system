from mongoengine import (
    Document, StringField, ReferenceField,
    DateTimeField, IntField, StringField
)
from datetime import datetime

# -------------------------------
# ผู้ใช้
# -------------------------------
class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

    meta = {"collection": "users"}

# -------------------------------
# โน้ต
# -------------------------------
class Note(Document):
    title = StringField(required=True)
    content = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User, required=True)
    status = StringField(default="Not Returned", choices=["Returned", "Not Returned"])  # สถานะการคืน

    meta = {"collection": "notes"}

# -------------------------------
# อุปกรณ์
# -------------------------------
class Equipment(Document):
    name = StringField(required=True, unique=True)   # ชื่ออุปกรณ์
    quantity = IntField(required=True, default=0)    # จำนวนคงเหลือ

    meta = {"collection": "equipment"}

# -------------------------------
# ประวัติการยืม
# -------------------------------
class BorrowRecord(Document):
    user = ReferenceField(User, required=True)            # ใครยืม
    equipment = ReferenceField(Equipment, required=True)  # อุปกรณ์อะไร
    amount = IntField(required=True, default=1)           # ยืมกี่ชิ้น
    borrowed_at = DateTimeField(default=datetime.utcnow)  # เวลาที่ยืม
    returned = IntField(default=0)                        # คืนแล้วกี่ชิ้น

    meta = {"collection": "borrow_records"}
