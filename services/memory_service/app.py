import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

memory_graphs = {
    "patient1": {
        "entities": [
            {"id": "e1", "type": "Person", "name": "Biren Das", "relation": "Self"},
            {"id": "e2", "type": "Person", "name": "Rahul Das", "relation": "Son", "city": "Guwahati", "phone": "9876543210"},
            {"id": "e3", "type": "Person", "name": "Dr. Barua", "relation": "Doctor", "clinic": "Shillong Civil Hospital"},
            {"id": "e4", "type": "Medicine", "name": "Donepezil 5mg", "time": "08:00 AM", "purpose": "Memory support"},
            {"id": "e5", "type": "Medicine", "name": "Amlodipine 5mg", "time": "02:00 PM", "purpose": "Blood pressure"}
        ],
        "relationships": [
            {"source": "Biren Das", "target": "Rahul Das", "edge": "HAS_SON"},
            {"source": "Rahul Das", "target": "Guwahati", "edge": "LIVES_IN"},
            {"source": "Biren Das", "target": "Dr. Barua", "edge": "CONSULTS"},
            {"source": "Biren Das", "target": "Donepezil 5mg", "edge": "TAKES_MORNING"},
            {"source": "Biren Das", "target": "Amlodipine 5mg", "edge": "TAKES_AFTERNOON"}
        ]
    }
}

reminders_db = {
    "patient1": [
        {"id": 1, "title": "Donepezil 5mg", "time": "08:00 AM", "type": "Medicine", "missed_count": 0, "status": "taken"},
        {"id": 2, "title": "Morning Walk in Garden", "time": "09:30 AM", "type": "Routine", "missed_count": 0, "status": "completed"},
        {"id": 3, "title": "Amlodipine 5mg", "time": "02:00 PM", "type": "Medicine", "missed_count": 3, "status": "missed"},
        {"id": 4, "title": "Call Son Rahul", "time": "06:00 PM", "type": "Routine", "missed_count": 0, "status": "pending"}
    ]
}

caregiver_alerts = []

memory_metrics = {
    "total_reminders_checked": 0,
    "total_sync_batches": 0,
    "active_alerts": 0
}

def evaluate_caregiver_alerts(patient_id, weekly_scores):
    alerts = []
    patient_reminders = reminders_db.get(patient_id, [])
    missed_medicines = sum(1 for r in patient_reminders if r["type"] == "Medicine" and r.get("missed_count", 0) >= 3)

    if missed_medicines > 0:
        alert_msg = f"Alert: Patient {patient_id} has missed medicine reminders 3 or more times."
        alerts.append({"type": "MISSED_MEDICINE", "severity": "HIGH", "message": alert_msg})

    if len(weekly_scores) >= 2:
        slope = (weekly_scores[-1] - weekly_scores[0]) / float(len(weekly_scores) - 1)
        if slope < -0.05:
            alert_msg = f"Alert: Weekly cognitive score slope dropped by {slope:.4f} (below threshold -0.05)."
            alerts.append({"type": "COGNITIVE_DECLINE", "severity": "CRITICAL", "message": alert_msg, "slope": slope})

    return alerts

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "memory-service", "status": "UP", "port": 5002}), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    memory_metrics["active_alerts"] = len(caregiver_alerts)
    return jsonify(memory_metrics), 200

@app.route("/api/memory-graph/<patient_id>", methods=["GET"])
def get_memory_graph(patient_id):
    graph = memory_graphs.get(patient_id, {"entities": [], "relationships": []})
    return jsonify({"patient_id": patient_id, "graph": graph}), 200

@app.route("/api/reminders/<patient_id>", methods=["GET"])
def get_reminders(patient_id):
    memory_metrics["total_reminders_checked"] += 1
    items = reminders_db.get(patient_id, [])
    return jsonify({"patient_id": patient_id, "reminders": items}), 200

@app.route("/api/reminders/status", methods=["POST"])
def update_reminder():
    data = request.get_json() or {}
    patient_id = data.get("patient_id", "patient1")
    reminder_id = data.get("id")
    status = data.get("status", "taken")

    items = reminders_db.get(patient_id, [])
    for item in items:
        if item["id"] == reminder_id:
            item["status"] = status
            if status == "missed":
                item["missed_count"] = item.get("missed_count", 0) + 1
            elif status == "taken":
                item["missed_count"] = 0
            return jsonify({"status": "updated", "reminder": item}), 200

    return jsonify({"error": "Reminder not found"}), 404

@app.route("/api/sync", methods=["POST"])
def sync_offline_records():
    data = request.get_json() or {}
    patient_id = data.get("patient_id", "patient1")
    offline_sessions = data.get("sessions", [])
    offline_reminders = data.get("reminders", [])
    weekly_scores = data.get("weekly_scores", [0.78, 0.74, 0.69])

    memory_metrics["total_sync_batches"] += 1

    triggered = evaluate_caregiver_alerts(patient_id, weekly_scores)
    for alert in triggered:
        caregiver_alerts.append(alert)

    return jsonify({
        "status": "synced",
        "synced_sessions": len(offline_sessions),
        "synced_reminders": len(offline_reminders),
        "alerts_triggered": triggered
    }), 200

@app.route("/api/caregiver/alerts", methods=["GET"])
def get_alerts():
    return jsonify({"alerts": caregiver_alerts}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
