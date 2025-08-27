from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User, Equipment, BorrowRecord
import re

notes = Blueprint("notes", __name__)

# ✅ Get all notes of current user
@notes.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    
    print(f"Fetching notes for user ID: {user_id}")
    
    all_notes = Note.objects(user=user).order_by("-created_at")
    print(f"Found {len(all_notes)} notes for user")
    
    notes_data = [
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": note.status
        }
        for note in all_notes
    ]
    
    print(f"Returning notes: {notes_data}")
    return jsonify(notes_data)

# ✅ Create note
@notes.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=user_id).first()
    
    try:
        # Parse equipment information from title
        title = data["title"]
        equipment_info = parse_equipment_from_title(title)
        
        print(f"Creating note with title: {title}")
        print(f"Parsed equipment info: {equipment_info}")
        
        # Create the note first
        note = Note(title=data["title"], content=data["content"], user=user, status="Not Returned")
        note.save()
        print(f"Note saved successfully with ID: {note.id}")
        
        # Update equipment quantities
        for equipment_name, quantity in equipment_info.items():
            equipment = Equipment.objects(name=equipment_name).first()
            if equipment:
                old_quantity = equipment.quantity
                equipment.quantity -= quantity
                equipment.save()
                print(f"Updated {equipment_name}: {old_quantity} -> {equipment.quantity}")
            else:
                print(f"Warning: Equipment '{equipment_name}' not found in database")
        
        return jsonify({
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "status": note.status,
            "equipment_updated": equipment_info
        }), 201
        
    except Exception as e:
        print(f"Error creating note: {str(e)}")
        return jsonify({"error": "Failed to create note", "details": str(e)}), 500

# ✅ Update note
@notes.route("/notes/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    data = request.get_json()

    try:
        # Find the note
        note = Note.objects(id=note_id, user=user).first()
        if not note:
            return jsonify({"msg": "Note not found or not yours"}), 404
        
        # Update status if provided
        if "status" in data:
            old_status = note.status
            note.status = data["status"]
            note.save()
            print(f"Updated note {note_id} status: {old_status} -> {note.status}")
            
            # If status is changed to "Returned", restore equipment quantities
            if old_status == "Not Returned" and data["status"] == "Returned":
                equipment_info = parse_equipment_from_title(note.title)
                for equipment_name, quantity in equipment_info.items():
                    equipment = Equipment.objects(name=equipment_name).first()
                    if equipment:
                        old_quantity = equipment.quantity
                        equipment.quantity += quantity
                        equipment.save()
                        print(f"Restored {equipment_name}: {old_quantity} -> {equipment.quantity}")
            
            # If status is changed from "Returned" to "Not Returned", reduce equipment quantities
            elif old_status == "Returned" and data["status"] == "Not Returned":
                equipment_info = parse_equipment_from_title(note.title)
                for equipment_name, quantity in equipment_info.items():
                    equipment = Equipment.objects(name=equipment_name).first()
                    if equipment:
                        old_quantity = equipment.quantity
                        equipment.quantity -= quantity
                        equipment.save()
                        print(f"Reduced {equipment_name}: {old_quantity} -> {equipment.quantity}")

        return jsonify({
            "msg": "Note updated!",
            "id": str(note.id),
            "status": note.status
        })
        
    except Exception as e:
        print(f"Error updating note: {str(e)}")
        return jsonify({"error": "Failed to update note", "details": str(e)}), 500

# ✅ Delete note
@notes.route("/notes/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    
    try:
        # Get the note before deleting to extract equipment info
        note = Note.objects(id=note_id, user=user).first()
        if not note:
            return jsonify({"msg": "Note not found or not yours"}), 404
        
        print(f"Deleting note with title: {note.title}")
        
        # Parse equipment information from title to restore quantities
        equipment_info = parse_equipment_from_title(note.title)
        print(f"Parsed equipment info for restoration: {equipment_info}")
        
        # Restore equipment quantities only if status is "Not Returned"
        if note.status == "Not Returned":
            for equipment_name, quantity in equipment_info.items():
                equipment = Equipment.objects(name=equipment_name).first()
                if equipment:
                    old_quantity = equipment.quantity
                    equipment.quantity += quantity
                    equipment.save()
                    print(f"Restored {equipment_name}: {old_quantity} -> {equipment.quantity}")
                else:
                    print(f"Warning: Equipment '{equipment_name}' not found when deleting note")
        else:
            print(f"Note status is '{note.status}', no equipment restoration needed")
        
        # Delete the note
        note.delete()
        print(f"Note deleted successfully")
        
        return jsonify({"msg": "Note deleted!", "equipment_restored": equipment_info if note.status == "Not Returned" else {}})
        
    except Exception as e:
        print(f"Error deleting note: {str(e)}")
        return jsonify({"error": "Failed to delete note", "details": str(e)}), 500

def parse_equipment_from_title(title):
    """Parse equipment names and quantities from note title"""
    equipment_info = {}
    
    # Extract equipment info from title format: "ยืม : ลูกฟุตบอล 2 ชิ้น, ลูกบาส 1 ชิ้น\nชื่อ : John Doe"
    if "ยืม :" in title:
        # Split by "ชื่อ :" to separate equipment part from borrower name
        parts = title.split("ชื่อ :")
        if len(parts) >= 2:
            equipment_part = parts[0].split("ยืม :")[1].strip()
            equipment_items = equipment_part.split(",")
            
            for item in equipment_items:
                item = item.strip()
                if "ชิ้น" in item:
                    # Extract name and quantity using regex
                    match = re.search(r'(.+?)\s+(\d+)\s*ชิ้น', item)
                    if match:
                        name = match.group(1).strip()
                        quantity = int(match.group(2))
                        equipment_info[name] = quantity
    
    return equipment_info
