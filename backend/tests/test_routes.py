import pytest
import sys, os
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
import json
from mongoengine import connect, disconnect
import mongomock

# ✅ เพิ่ม path ให้ python หา backend ได้
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Flask app หลัก
from models import User, Equipment, BorrowRecord, Note


@pytest.fixture(autouse=True)
def clean_db():
    """ล้าง DB ก่อนและหลังเทส"""
    try:
        disconnect()
    except Exception:
        pass

    mock_client = mongomock.MongoClient(uuidRepresentation="standard")
    connect(
        db='testdb',
        alias='default',
        host='mongodb://localhost',
        mongo_client_class=lambda *args, **kwargs: mock_client
    )

    for coll in (User, Equipment, BorrowRecord, Note):
        try:
            coll.drop_collection()
        except Exception:
            pass

    yield

    for coll in (User, Equipment, BorrowRecord, Note):
        try:
            coll.drop_collection()
        except Exception:
            pass
    disconnect()


@pytest.fixture
def client():
    return app.test_client()


def register_and_login(client, username="testuser", password="testpass"):
    """สมัครและล็อกอินเพื่อให้ได้ token"""
    client.post("/auth/register", json={"username": username, "password": password})
    res = client.post("/auth/login", json={"username": username, "password": password})
    assert res.status_code == 200, f"Login failed: {res.get_json()}"
    token = res.get_json()["access_token"]
    return token


# -------------------------------
# Auth Tests
# -------------------------------
def test_register_and_login(client):
    # Register
    res = client.post("/auth/register", json={"username": "u1", "password": "p1"})
    assert res.status_code == 200

    # Duplicate register
    res2 = client.post("/auth/register", json={"username": "u1", "password": "p1"})
    assert res2.status_code == 400

    # Login wrong
    res3 = client.post("/auth/login", json={"username": "u1", "password": "wrong"})
    assert res3.status_code == 401

    # Login correct
    res4 = client.post("/auth/login", json={"username": "u1", "password": "p1"})
    assert res4.status_code == 200
    assert "access_token" in res4.get_json()


# -------------------------------
# Equipment Tests
# -------------------------------
def test_add_and_get_equipment(client):
    token = register_and_login(client)

    # Add equipment
    res = client.post(
        "/api/equipment/add",
        json={"name": "ลูกฟุตบอล", "quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 201

    # Duplicate add
    res2 = client.post(
        "/api/equipment/add",
        json={"name": "ลูกฟุตบอล", "quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res2.status_code == 400

    # Get list
    res3 = client.get("/api/equipment", headers={"Authorization": f"Bearer {token}"})
    data = res3.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "ลูกฟุตบอล"

    # Public endpoint
    res4 = client.get("/api/equipment/public")
    assert res4.status_code == 200
    assert res4.get_json()[0]["name"] == "ลูกฟุตบอล"


def test_borrow_and_return_equipment(client):
    token = register_and_login(client)

    # Add equipment
    client.post(
        "/api/equipment/add",
        json={"name": "ลูกบาส", "quantity": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    equipment_id = str(Equipment.objects.first().id)

    # Borrow
    res2 = client.post(
        "/api/equipment/borrow",
        json={"equipment_id": equipment_id, "amount": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res2.status_code == 200
    eq = Equipment.objects.first()
    assert eq.quantity == 1

    record = BorrowRecord.objects.first()
    record_id = str(record.id)

    # Return
    res3 = client.post(
        "/api/equipment/return",
        json={"record_id": record_id, "amount": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res3.status_code == 200
    eq.reload()
    assert eq.quantity == 2


# -------------------------------
# Notes Tests
# -------------------------------
def test_create_update_delete_note_with_equipment(client):
    token = register_and_login(client)

    # Add equipment first
    client.post(
        "/api/equipment/add",
        json={"name": "ลูกวอลเลย์บอล", "quantity": 4},
        headers={"Authorization": f"Bearer {token}"}
    )

    # Create note that borrows equipment
    title = "ยืม : ลูกวอลเลย์บอล 2 ชิ้น\nชื่อ : John"
    res = client.post(
        "/api/notes",
        json={"title": title, "content": "ใช้สำหรับแข่งขัน"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 201
    note_id = res.get_json()["id"]

    eq = Equipment.objects.first()
    assert eq.quantity == 2  # quantity ลดลง

    # Update note status -> Returned
    res2 = client.put(
        f"/api/notes/{note_id}",
        json={"status": "Returned"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res2.status_code == 200
    eq.reload()
    assert eq.quantity == 4  # คืนครบ

    # Delete note (status Returned -> no restore)
    res3 = client.delete(
        f"/api/notes/{note_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res3.status_code == 200
    eq.reload()
    assert eq.quantity == 4
