# routes/equipment.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Equipment, BorrowRecord, User

equipment_bp = Blueprint("equipment", __name__)

# ✅ ดูรายการอุปกรณ์
@equipment_bp.route("/equipment", methods=["GET"])
@jwt_required()
def get_equipment():
    items = Equipment.objects()
    return jsonify([
        {"id": str(item.id), "name": item.name, "quantity": item.quantity}
        for item in items
    ]), 200

# ✅ Get equipment data for frontend (no auth required for public display)
@equipment_bp.route("/equipment/public", methods=["GET"])
def get_equipment_public():
    items = Equipment.objects()
    return jsonify([
        {"name": item.name, "quantity": item.quantity}
        for item in items
    ]), 200

# ✅ เพิ่มอุปกรณ์ใหม่
@equipment_bp.route("/equipment/add", methods=["POST"])
@jwt_required()
def add_equipment():
    data = request.get_json()
    name = data.get("name")
    quantity = data.get("quantity", 0)

    if not name:
        return jsonify({"msg": "กรุณาระบุชื่ออุปกรณ์"}), 400

    if Equipment.objects(name=name).first():
        return jsonify({"msg": "มีอุปกรณ์นี้แล้ว"}), 400

    equipment = Equipment(name=name, quantity=quantity)
    equipment.save()

    return jsonify({"msg": "เพิ่มอุปกรณ์สำเร็จ"}), 201

# ✅ ยืมอุปกรณ์
@equipment_bp.route("/equipment/borrow", methods=["POST"])
@jwt_required()
def borrow_equipment():
    data = request.get_json()
    equipment_id = data.get("equipment_id")
    amount = data.get("amount", 1)

    equipment = Equipment.objects(id=equipment_id).first()
    if not equipment:
        return jsonify({"msg": "ไม่พบอุปกรณ์"}), 404

    if equipment.quantity < amount:
        return jsonify({"msg": "อุปกรณ์ไม่เพียงพอ"}), 400

    # ลดจำนวนคงเหลือ
    equipment.quantity -= amount
    equipment.save()

    # บันทึกการยืม
    user = User.objects(username=get_jwt_identity()).first()
    borrow_record = BorrowRecord(user=user, equipment=equipment, amount=amount)
    borrow_record.save()

    return jsonify({"msg": "ยืมอุปกรณ์สำเร็จ"}), 200

# ✅ คืนอุปกรณ์
@equipment_bp.route("/equipment/return", methods=["POST"])
@jwt_required()
def return_equipment():
    data = request.get_json()
    record_id = data.get("record_id")
    amount = data.get("amount", 1)

    record = BorrowRecord.objects(id=record_id).first()
    if not record:
        return jsonify({"msg": "ไม่พบบันทึกการยืม"}), 404

    if amount > (record.amount - record.returned):
        return jsonify({"msg": "จำนวนคืนไม่ถูกต้อง"}), 400

    # อัปเดตบันทึก
    record.returned += amount
    record.save()

    # เพิ่มจำนวนอุปกรณ์กลับ
    equipment = record.equipment
    equipment.quantity += amount
    equipment.save()

    return jsonify({"msg": "คืนอุปกรณ์สำเร็จ"}), 200
