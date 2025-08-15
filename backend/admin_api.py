# # admin_api.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pymysql
# import flask import
# import os
# from werkzeug.security import generate_password_hash

# admin_bp = Blueprint("admin", __name__)
# CORS(admin_bp)

# # Database connection details (override with environment variables in production)
# DB_HOST = os.getenv("DB_HOST", "localhost")
# DB_USER = os.getenv("DB_USER", "root")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "")
# DB_NAME = os.getenv("DB_NAME", "flask_notes_app")  # change to your DB name if needed
# DB_CHARSET = "utf8mb4"


# def get_db_connection():
#     return pymysql.connect(
#         host=DB_HOST,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME,
#         cursorclass=pymysql.cursors.DictCursor,
#         charset=DB_CHARSET
#     )


# # ---------------------------
# # Helper functions
# # ---------------------------
# def safe_close(conn):
#     try:
#         conn.close()
#     except Exception:
#         pass


# # ---------------------------
# # User management endpoints
# # ---------------------------

# @admin_bp.route("/users", methods=["GET"])
# def get_users():
#     """Return list of all users (admins can use this to manage accounts)."""
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY id ASC")
#             users = cursor.fetchall()
#         return jsonify(users), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/users/<int:user_id>", methods=["GET"])
# def get_user(user_id):
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT id, username, email, role, created_at FROM users WHERE id = %s", (user_id,))
#             user = cursor.fetchone()
#         if not user:
#             return jsonify({"error": "User not found"}), 404
#         return jsonify(user), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/users", methods=["POST"])
# def create_user():
#     """Create a new user (admin or normal user). Password will be hashed."""
#     data = request.get_json() or {}
#     username = data.get("username")
#     email = data.get("email")
#     password = data.get("password")
#     role = data.get("role", "user")

#     if not username or not email or not password:
#         return jsonify({"error": "username, email and password are required"}), 400

#     password_hash = generate_password_hash(password)

#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             try:
#                 cursor.execute(
#                     "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
#                     (username, email, password_hash, role)
#                 )
#                 conn.commit()
#                 new_id = cursor.lastrowid
#             except pymysql.err.IntegrityError as e:
#                 # likely duplicate username/email
#                 return jsonify({"error": "Username or email already exists", "details": str(e)}), 400

#         return jsonify({"message": "User created", "user_id": new_id}), 201
#     finally:
#         safe_close(conn)


# @app.route("/admin/users/<int:user_id>", methods=["PUT"])
# def update_user(user_id):
#     """
#     Update a user's username, email, role, or password.
#     To change password, include 'password' in JSON body (will be hashed).
#     """
#     data = request.get_json() or {}
#     username = data.get("username")
#     email = data.get("email")
#     role = data.get("role")
#     password = data.get("password")

#     if not any([username, email, role, password]):
#         return jsonify({"error": "At least one field (username, email, role, password) is required"}), 400

#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             # Check user exists
#             cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
#             if cursor.fetchone() is None:
#                 return jsonify({"error": "User not found"}), 404

#             # Build dynamic update statement
#             fields = []
#             values = []
#             if username:
#                 fields.append("username = %s")
#                 values.append(username)
#             if email:
#                 fields.append("email = %s")
#                 values.append(email)
#             if role:
#                 fields.append("role = %s")
#                 values.append(role)
#             if password:
#                 fields.append("password_hash = %s")
#                 values.append(generate_password_hash(password))

#             values.append(user_id)
#             sql = "UPDATE users SET " + ", ".join(fields) + " WHERE id = %s"
#             try:
#                 cursor.execute(sql, tuple(values))
#                 conn.commit()
#             except pymysql.err.IntegrityError as e:
#                 return jsonify({"error": "Integrity error (possible duplicate username/email)", "details": str(e)}), 400

#         return jsonify({"message": "User updated"}), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/users/<int:user_id>", methods=["DELETE"])
# def delete_user(user_id):
#     """Delete a user and cascade-delete their ideas (if FK ON DELETE CASCADE set)."""
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
#             if cursor.fetchone() is None:
#                 return jsonify({"error": "User not found"}), 404

#             # Optionally: prevent deleting the last admin, or self-delete protection - not implemented here
#             cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#             conn.commit()

#         return jsonify({"message": "User deleted"}), 200
#     finally:
#         safe_close(conn)


# # ---------------------------
# # Idea management endpoints
# # ---------------------------

# @app.route("/admin/ideas", methods=["GET"])
# def get_ideas():
#     """
#     Get all ideas. Optional query param:
#       ?status=pending|approved|disapproved - to filter by status
#     Returns idea meta including creator username/email.
#     """
#     status = request.args.get("status")  # optional
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             if status and status.lower() in ("pending", "approved", "disapproved"):
#                 cursor.execute("""
#                     SELECT ideas.id, ideas.title, ideas.description, ideas.status, ideas.created_at,
#                            users.id AS user_id, users.username, users.email
#                     FROM ideas
#                     JOIN users ON ideas.user_id = users.id
#                     WHERE ideas.status = %s
#                     ORDER BY ideas.created_at DESC
#                 """, (status.lower(),))
#             else:
#                 cursor.execute("""
#                     SELECT ideas.id, ideas.title, ideas.description, ideas.status, ideas.created_at,
#                            users.id AS user_id, users.username, users.email
#                     FROM ideas
#                     JOIN users ON ideas.user_id = users.id
#                     ORDER BY ideas.created_at DESC
#                 """)
#             rows = cursor.fetchall()
#         return jsonify(rows), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/ideas/<int:idea_id>", methods=["GET"])
# def get_idea(idea_id):
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("""
#                 SELECT ideas.id, ideas.title, ideas.description, ideas.status, ideas.created_at,
#                        users.id AS user_id, users.username, users.email
#                 FROM ideas
#                 JOIN users ON ideas.user_id = users.id
#                 WHERE ideas.id = %s
#             """, (idea_id,))
#             idea = cursor.fetchone()
#             if not idea:
#                 return jsonify({"error": "Idea not found"}), 404
#         return jsonify(idea), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/ideas/<int:idea_id>/approve", methods=["PUT"])
# def approve_idea(idea_id):
#     """Approve an idea (status -> 'approved')."""
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT status FROM ideas WHERE id = %s", (idea_id,))
#             row = cursor.fetchone()
#             if not row:
#                 return jsonify({"error": "Idea not found"}), 404

#             cursor.execute("UPDATE ideas SET status = 'approved' WHERE id = %s", (idea_id,))
#             conn.commit()
#         return jsonify({"message": "Idea approved"}), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/ideas/<int:idea_id>/disapprove", methods=["PUT"])
# def disapprove_idea(idea_id):
#     """Disapprove an idea (status -> 'disapproved')."""
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT status FROM ideas WHERE id = %s", (idea_id,))
#             row = cursor.fetchone()
#             if not row:
#                 return jsonify({"error": "Idea not found"}), 404

#             cursor.execute("UPDATE ideas SET status = 'disapproved' WHERE id = %s", (idea_id,))
#             conn.commit()
#         return jsonify({"message": "Idea disapproved"}), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/ideas/<int:idea_id>", methods=["DELETE"])
# def delete_idea(idea_id):
#     """Delete any idea (admin privilege)."""
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT id FROM ideas WHERE id = %s", (idea_id,))
#             if cursor.fetchone() is None:
#                 return jsonify({"error": "Idea not found"}), 404

#             cursor.execute("DELETE FROM ideas WHERE id = %s", (idea_id,))
#             conn.commit()
#         return jsonify({"message": "Idea deleted"}), 200
#     finally:
#         safe_close(conn)


# @app.route("/admin/ideas/<int:idea_id>", methods=["PUT"])
# def update_idea_admin(idea_id):
#     """
#     Optionally let admin edit idea content/title.
#     JSON body: { "title": "...", "description": "...", "status": "approved|pending|disapproved" (optional) }
#     """
#     data = request.get_json() or {}
#     title = data.get("title")
#     description = data.get("description")
#     status = data.get("status")  # optional

#     if not any([title, description, status]):
#         return jsonify({"error": "At least one field (title, description, status) is required"}), 400

#     allowed_status = {"pending", "approved", "disapproved"}
#     if status and status not in allowed_status:
#         return jsonify({"error": f"Invalid status, must be one of {allowed_status}"}), 400

#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute("SELECT id FROM ideas WHERE id = %s", (idea_id,))
#             if cursor.fetchone() is None:
#                 return jsonify({"error": "Idea not found"}), 404

#             fields = []
#             values = []
#             if title:
#                 fields.append("title = %s")
#                 values.append(title)
#             if description:
#                 fields.append("description = %s")
#                 values.append(description)
#             if status:
#                 fields.append("status = %s")
#                 values.append(status)
#             values.append(idea_id)
#             sql = "UPDATE ideas SET " + ", ".join(fields) + " WHERE id = %s"
#             cursor.execute(sql, tuple(values))
#             conn.commit()
#         return jsonify({"message": "Idea updated by admin"}), 200
#     finally:
#         safe_close(conn)


# # ---------------------------
# # (Optional) Admin logs endpoint
# # ---------------------------
# @app.route("/admin/logs", methods=["GET"])
# def get_admin_logs():
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             # If admin_logs table doesn't exist, return empty list
#             try:
#                 cursor.execute("""
#                     SELECT l.id, l.action, l.timestamp, a.username AS admin_username, 
#                            tu.username AS target_username
#                     FROM admin_logs l
#                     LEFT JOIN users a ON l.admin_id = a.id
#                     LEFT JOIN users tu ON l.target_user_id = tu.id
#                     ORDER BY l.timestamp DESC
#                 """)
#                 logs = cursor.fetchall()
#             except pymysql.err.ProgrammingError:
#                 logs = []
#         return jsonify(logs), 200
#     finally:
#         safe_close(conn)


# # ---------------------------
# # Run
# # ---------------------------
# if __name__ == "__main__":
#     # In production, run with a production server (gunicorn/uwsgi)
#     app.run(debug=True, host="0.0.0.0", port=int(os.getenv("ADMIN_API_PORT", 5001)))
