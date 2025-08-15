# admin_users_api.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import pymysql
import os
from werkzeug.security import generate_password_hash

admin_users_bp = Blueprint("admin_users", __name__)
CORS(admin_users_bp)

# DB connection
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "flask_notes_app")
DB_CHARSET = "utf8mb4"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        charset=DB_CHARSET
    )

def safe_close(conn):
    try:
        conn.close()
    except:
        pass

# ---------------------------
# User Management
# ---------------------------
@admin_users_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY id ASC")
            return jsonify(cursor.fetchall()), 200
    finally:
        safe_close(conn)

@admin_users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, email, role, created_at FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    finally:
        safe_close(conn)

@admin_users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not email or not password:
        return jsonify({"error": "username, email and password are required"}), 400

    password_hash = generate_password_hash(password)

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                    (username, email, password_hash, role)
                )
                conn.commit()
                return jsonify({"message": "User created", "user_id": cursor.lastrowid}), 201
            except pymysql.err.IntegrityError as e:
                return jsonify({"error": "Username or email already exists", "details": str(e)}), 400
    finally:
        safe_close(conn)

@admin_users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    if not any([username, email, role, password]):
        return jsonify({"error": "At least one field is required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            if cursor.fetchone() is None:
                return jsonify({"error": "User not found"}), 404

            fields = []
            values = []
            if username:
                fields.append("username = %s")
                values.append(username)
            if email:
                fields.append("email = %s")
                values.append(email)
            if role:
                fields.append("role = %s")
                values.append(role)
            if password:
                fields.append("password_hash = %s")
                values.append(generate_password_hash(password))

            values.append(user_id)
            cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = %s", tuple(values))
            conn.commit()
        return jsonify({"message": "User updated"}), 200
    finally:
        safe_close(conn)

@admin_users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
            if cursor.fetchone() is None:
                return jsonify({"error": "User not found"}), 404
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
        return jsonify({"message": "User deleted"}), 200
    finally:
        safe_close(conn)
