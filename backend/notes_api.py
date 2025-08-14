from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime

notes_bp = Blueprint('notes_api', __name__)

# Database connection helper
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="secure_notes_app",
        cursorclass=pymysql.cursors.DictCursor
    )

# Add a new note (pending approval by default)
@notes_bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')  # Ideally from JWT session, but for now pass it

    if not title or not content or not user_id:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ide (title, content, user_id, is_approved, created_at) VALUES (%s, %s, %s, %s, %s)",
        (title, content, user_id, 0, datetime.now())
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Note created successfully. Awaiting admin approval."}), 201


# Get all approved notes (public feed)
@notes_bp.route('/notes', methods=['GET'])
def get_approved_notes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT notes.id, title, content, users.username, created_at FROM notes JOIN users ON notes.user_id = users.id WHERE is_approved = 1 ORDER BY created_at DESC")
    notes = cursor.fetchall()
    conn.close()
    return jsonify(notes), 200


# Get notes for a specific user (both approved & pending)
@notes_bp.route('/notes/user/<int:user_id>', methods=['GET'])
def get_user_notes(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    notes = cursor.fetchall()
    conn.close()
    return jsonify(notes), 200


# Edit a note (only if not approved yet)
@notes_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = %s AND user_id = %s", (note_id, user_id))
    note = cursor.fetchone()

    if not note:
        conn.close()
        return jsonify({"error": "Note not found or not owned by user"}), 404

    if note['is_approved'] == 1:
        conn.close()
        return jsonify({"error": "Approved notes cannot be edited"}), 403

    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (title, content, note_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note updated successfully"}), 200


# Delete a note (only if not approved yet)
@notes_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    user_id = request.args.get('user_id')  # Could come from JWT token
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = %s AND user_id = %s", (note_id, user_id))
    note = cursor.fetchone()

    if not note:
        conn.close()
        return jsonify({"error": "Note not found or not owned by user"}), 404

    if note['is_approved'] == 1:
        conn.close()
        return jsonify({"error": "Approved notes cannot be deleted"}), 403

    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note deleted successfully"}), 200
