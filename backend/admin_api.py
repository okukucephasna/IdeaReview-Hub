from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL connection function
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="notes_app",
        cursorclass=pymysql.cursors.DictCursor
    )

# ----------- USER MANAGEMENT -----------

@app.route("/admin/users", methods=["GET"])
def get_all_users():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, username, email, role FROM users")
        users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route("/admin/user/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    data = request.json
    username = data.get("username")
    email = data.get("email")
    role = data.get("role")

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE users
            SET username=%s, email=%s, role=%s
            WHERE id=%s
        """, (username, email, role, user_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "User updated successfully"})

@app.route("/admin/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "User deleted successfully"})

# ----------- NOTE MANAGEMENT -----------

@app.route("/admin/notes", methods=["GET"])
def get_all_notes():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT notes.id, notes.content, notes.status, users.username
            FROM notes
            JOIN users ON notes.user_id = users.id
        """)
        notes = cursor.fetchall()
    conn.close()
    return jsonify(notes)

@app.route("/admin/note/<int:note_id>/approve", methods=["PUT"])
def approve_note(note_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE notes SET status='approved' WHERE id=%s", (note_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note approved"})

@app.route("/admin/note/<int:note_id>/disapprove", methods=["PUT"])
def disapprove_note(note_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE notes SET status='disapproved' WHERE id=%s", (note_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note disapproved"})

@app.route("/admin/note/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM notes WHERE id=%s", (note_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Note deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
