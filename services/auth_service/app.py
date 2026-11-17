import os
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.environ.get("SECRET_KEY", "smrithi-secret-key-2026")

users_db = {
    "patient1": {"password": "pass123", "role": "patient", "name": "Biren Das", "lang": "as"},
    "caregiver1": {"password": "pass123", "role": "caregiver", "name": "Rahul Das", "patient_id": "patient1"}
}

auth_metrics = {
    "total_logins": 0,
    "active_tokens": 0
}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "auth-service", "status": "UP", "port": 5000}), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    return jsonify(auth_metrics), 200

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    user = users_db.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": username,
        "role": user["role"],
        "name": user["name"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    auth_metrics["total_logins"] += 1
    auth_metrics["active_tokens"] += 1

    return jsonify({
        "token": token,
        "username": username,
        "name": user["name"],
        "role": user["role"]
    }), 200

@app.route("/api/verify", methods=["POST"])
def verify():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"valid": False, "error": "No token provided"}), 401
    
    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "user": decoded}), 200
    except Exception as err:
        return jsonify({"valid": False, "error": str(err)}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
