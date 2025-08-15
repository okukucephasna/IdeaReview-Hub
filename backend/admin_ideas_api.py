# admin_ideas_api.py
from flask import Blueprint, request, jsonify
from flask_cors import CORS
import pymysql
import os

admin_ideas_bp = Blueprint("admin_ideas", __name__)
CORS(admin_ideas_bp)

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
# Idea Management
# ---------------------------
@admin_ideas_bp.route("/ideas", methods=["GET"])
def get_ideas():
    status = request.args.get("status")
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if status and status.lower() in ("pending", "approved", "disapproved"):
                cursor.execute("""
                    SELECT ideas.id, ideas.title, ideas.description, ideas.status, ideas.created_at,
                           users.id AS user_id, users.username, users.email
                    FROM ideas
                    JOIN users ON ideas.user_id = users.id
                    WHERE ideas.status = %s
                    ORDER BY ideas.created_at DESC
                """, (status.lower(),))
            else:
                cursor.execute("""
                    SELECT ideas.id, ideas.title, ideas.description, ideas.status, ideas.created_at,
                           users.id AS user_id, users.username, users.email
                    FROM ideas
                    JOIN users ON ideas.user_id = users.id
                    ORDER BY ideas.created_at DESC
                """)
            return jsonify(cursor.fetchall()), 200
    finally:
        safe_close(conn)

@admin_ideas_bp.route("/ideas/<int:idea_id>", methods=["GET"])
def get_idea(idea_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT ideas.id, ideas.title, ideas.description, ideas.status, ideas.created_at,
                       users.id AS user_id, users.username, users.email
                FROM ideas
                JOIN users ON ideas.user_id = users.id
                WHERE ideas.id = %s
            """, (idea_id,))
            idea = cursor.fetchone()
        if not idea:
            return jsonify({"error": "Idea not found"}), 404
        return jsonify(idea), 200
    finally:
        safe_close(conn)

@admin_ideas_bp.route("/ideas/<int:idea_id>/approve", methods=["PUT"])
def approve_idea(idea_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE ideas SET status = 'approved' WHERE id = %s", (idea_id,))
            conn.commit()
        return jsonify({"message": "Idea approved"}), 200
    finally:
        safe_close(conn)

@admin_ideas_bp.route("/ideas/<int:idea_id>/disapprove", methods=["PUT"])
def disapprove_idea(idea_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE ideas SET status = 'disapproved' WHERE id = %s", (idea_id,))
            conn.commit()
        return jsonify({"message": "Idea disapproved"}), 200
    finally:
        safe_close(conn)

@admin_ideas_bp.route("/ideas/<int:idea_id>", methods=["PUT"])
def update_idea(idea_id):
    data = request.get_json() or {}
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    if not any([title, description, status]):
        return jsonify({"error": "At least one field is required"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            fields = []
            values = []
            if title:
                fields.append("title = %s")
                values.append(title)
            if description:
                fields.append("description = %s")
                values.append(description)
            if status:
                fields.append("status = %s")
                values.append(status)

            values.append(idea_id)
            cursor.execute(f"UPDATE ideas SET {', '.join(fields)} WHERE id = %s", tuple(values))
            conn.commit()
        return jsonify({"message": "Idea updated"}), 200
    finally:
        safe_close(conn)

@admin_ideas_bp.route("/ideas/<int:idea_id>", methods=["DELETE"])
def delete_idea(idea_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM ideas WHERE id = %s", (idea_id,))
            conn.commit()
        return jsonify({"message": "Idea deleted"}), 200
    finally:
        safe_close(conn)
