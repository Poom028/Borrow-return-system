from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note, User

notes = Blueprint("notes", __name__)

# ✅ Get all notes of current user
@notes.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    all_notes = Note.objects(user=user).order_by("-created_at")
    return jsonify([
        {
            "id": str(note.id),
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for note in all_notes
    ])

# ✅ Create note
@notes.route("/notes", methods=["POST"])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=user_id).first()
    note = Note(title=data["title"], content=data["content"], user=user)
    note.save()
    return jsonify({
        "id": str(note.id),
        "title": note.title,
        "content": note.content,
        "created_at": note.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 201

# ✅ Update note
@notes.route("/notes/<note_id>", methods=["PUT"])
@jwt_required()
def update_note(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    data = request.get_json()

    updated = Note.objects(id=note_id, user=user).update_one(
        **{k: v for k, v in data.items() if k in ["title", "content"]}
    )
    if not updated:
        return jsonify({"msg": "Note not found or not yours"}), 404

    return jsonify({"msg": "Note updated!"})

# ✅ Delete note
@notes.route("/notes/<note_id>", methods=["DELETE"])
@jwt_required()
def delete_note(note_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    deleted = Note.objects(id=note_id, user=user).delete()
    if not deleted:
        return jsonify({"msg": "Note not found or not yours"}), 404
    return jsonify({"msg": "Note deleted!"})
