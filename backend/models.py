# models.py
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

class Note(Document):
    title = StringField(required=True)
    content = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    user = ReferenceField(User)

# -------------------------------
# ✅ เพิ่มใหม่: อุปกรณ์และการยืม
# -------------------------------
class Equipment(Document):
    name = StringField(required=True, unique=True)  # ชื่ออุปกรณ์
    quantity = IntField(required=True, default=0)   # จำนวนคงเหลือ

class BorrowRecord(Document):
    user = ReferenceField(User, required=True)           # ใครยืม
    equipment = ReferenceField(Equipment, required=True) # อุปกรณ์อะไร
    amount = IntField(required=True, default=1)          # ยืมกี่ชิ้น
    borrowed_at = DateTimeField(default=datetime.utcnow) # เวลาที่ยืม
    returned = IntField(default=0)                       # คืนแล้วกี่ชิ้น
