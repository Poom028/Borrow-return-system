from flask import Blueprint, request, jsonify
from models import User
from flask_jwt_extended import (
    create_access_token, jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

auth = Blueprint("auth", __name__)

# --------------------------
# Register
# --------------------------
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if User.objects(username=data["username"]):
        return jsonify({"msg": "Username already exists"}), 400

    hashed_pw = generate_password_hash(data["password"])
    user = User(username=data["username"], password=hashed_pw)
    user.save()

    return jsonify({"msg": "User registered successfully"}), 201

# --------------------------
# Login
# --------------------------
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.objects(username=data["username"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "Invalid credentials"}), 401

    # สร้าง token ที่มีอายุ 1 ชั่วโมง
    token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=1)
    )

    return jsonify({
        "access_token": token,
        "username": user.username
    })

# --------------------------
# Logout (สำหรับ JWT)
# --------------------------
@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    ใน JWT logout จริง ๆ ต้องทำฝั่ง client (ลบ token ออกจาก storage)
    ถ้าอยาก block token ต้องใช้ JWT Blocklist
    """
    user_id = get_jwt_identity()
    return jsonify({"msg": f"User {user_id} logged out (client should discard token)"}), 200
