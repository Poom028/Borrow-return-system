# tests/test_routes.py
import pytest
import mongomock
from mongoengine import connect, disconnect
from app import app
import models
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ---------- Fixtures ----------
@pytest.fixture(autouse=True)
def mock_db():
    """ใช้ mongomock แทน MongoDB จริง"""
    disconnect()
    mock_client = mongomock.MongoClient()
    connect("testdb", host="mongodb://localhost", mongo_client_class=lambda *a, **kw: mock_client)
    # เคลียร์ collection
    for coll in (models.User, models.Equipment, models.Note, models.BorrowRecord):
        try:
            coll.drop_collection()
        except Exception:
            pass
    yield
    disconnect()

@pytest.fixture
def client():
    return app.test_client()

def auth_header(token):
    return {"Authorization": f"Bearer {token}"}

# ---------- Helper ----------
def register_and_login(client, username="alice", password="secret123"):
    """สมัครสมาชิกและ login → คืน access token"""
    client.post("/api/register", json={"username": username, "password": password})
    resp = client.post("/api/login", json={"username": username, "password": password})
    return resp.get_json()["access_token"]

# ---------- Tests ----------

def test_register_and_login(client):
    token = register_and_login(client)
    assert token is not None

def test_equipment_crud_and_borrow_return(client):
    token = register_and_login(client)

    # เพิ่มอุปกรณ์
    resp = client.post("/api/equipment/add",
                       json={"name": "ลูกฟุตบอล", "quantity": 5},
                       headers=auth_header(token))
    assert resp.status_code == 201

    # ดึงข้อมูลอุปกรณ์
    resp = client.get("/api/equipment", headers=auth_header(token))
    data = resp.get_json()
    assert len(data) == 1
    equipment_id = data[0]["id"]
    assert data[0]["quantity"] == 5

    # ยืมอุปกรณ์
    resp = client.post("/api/equipment/borrow",
                       json={"equipment_id": equipment_id, "amount": 2},
                       headers=auth_header(token))
    assert resp.status_code == 200

    # ตรวจสอบจำนวนลดลง
    resp = client.get("/api/equipment", headers=auth_header(token))
    assert resp.get_json()[0]["quantity"] == 3

    # คืนอุปกรณ์
    record = models.BorrowRecord.objects.first()
    resp = client.post("/api/equipment/return",
                       json={"record_id": str(record.id), "amount": 2},
                       headers=auth_header(token))
    assert resp.status_code == 200

    # ตรวจสอบจำนวนกลับมาเท่าเดิม
    resp = client.get("/api/equipment", headers=auth_header(token))
    assert resp.get_json()[0]["quantity"] == 5

def test_notes_affect_equipment(client):
    token = register_and_login(client)

    # เพิ่มอุปกรณ์
    client.post("/api/equipment/add",
                json={"name": "ลูกฟุตบอล", "quantity": 5},
                headers=auth_header(token))

    # ตรวจสอบ quantity เริ่มต้น
    resp = client.get("/api/equipment", headers=auth_header(token))
    equipment_id = resp.get_json()[0]["id"]
    assert resp.get_json()[0]["quantity"] == 5

    # สร้างบันทึก (ยืมลูกฟุตบอล 2 ชิ้น)
    title = "ยืม : ลูกฟุตบอล 2 ชิ้น\nชื่อ : John Doe"
    resp = client.post("/api/notes",
                       json={"title": title, "content": "borrow football"},
                       headers=auth_header(token))
    assert resp.status_code == 201
    note_id = resp.get_json()["id"]

    # ตรวจสอบ quantity ลดลง
    resp = client.get("/api/equipment", headers=auth_header(token))
    assert resp.get_json()[0]["quantity"] == 3  # 5-2

    # อัปเดตสถานะบันทึก → Returned
    resp = client.put(f"/api/notes/{note_id}",
                      json={"status": "Returned"},
                      headers=auth_header(token))
    assert resp.status_code == 200

    # ตรวจสอบ quantity กลับมาเท่าเดิม
    resp = client.get("/api/equipment", headers=auth_header(token))
    assert resp.get_json()[0]["quantity"] == 5

    # ลบบันทึก
    resp = client.delete(f"/api/notes/{note_id}", headers=auth_header(token))
    assert resp.status_code == 200

    # ตรวจสอบ quantity ยังคงเท่าเดิม
    resp = client.get("/api/equipment", headers=auth_header(token))
    assert resp.get_json()[0]["quantity"] == 5

# ---------- Edge cases ----------
def test_borrow_return_edge_cases(client):
    token = register_and_login(client)

    # เพิ่มอุปกรณ์ 5 ชิ้น
    client.post("/api/equipment/add",
                json={"name": "ลูกฟุตบอล", "quantity": 5},
                headers=auth_header(token))
    equipment = models.Equipment.objects.first()

    # ยืมเกินจำนวน
    resp = client.post("/api/equipment/borrow",
                       json={"equipment_id": str(equipment.id), "amount": 10},
                       headers=auth_header(token))
    assert resp.status_code == 400

    # ยืม 3 ชิ้น
    resp = client.post("/api/equipment/borrow",
                       json={"equipment_id": str(equipment.id), "amount": 3},
                       headers=auth_header(token))
    assert resp.status_code == 200
    record = models.BorrowRecord.objects.first()

    # คืนเกินจำนวน
    resp = client.post("/api/equipment/return",
                       json={"record_id": str(record.id), "amount": 5},
                       headers=auth_header(token))
    assert resp.status_code == 400

    # คืนปกติ
    resp = client.post("/api/equipment/return",
                       json={"record_id": str(record.id), "amount": 3},
                       headers=auth_header(token))
    assert resp.status_code == 200

    # ตรวจสอบ quantity กลับมาครบ
    equipment.reload()
    assert equipment.quantity == 5
