from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
from admin_users_api import admin_users_bp
from admin_ideas_api import admin_ideas_bp
# Import your API routes
import admin_api  # make sure admin_api.py has a Blueprint

app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)  # Enable CORS if React fetches from another origin
# app.py

# Register Blueprints
app.register_blueprint(admin_users_bp, url_prefix="/api/admin")
app.register_blueprint(admin_ideas_bp, url_prefix="/api/admin")

# Register API blueprint
app.register_blueprint(admin_api.admin_bp, url_prefix="/api/admin")

# Serve React frontend
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
