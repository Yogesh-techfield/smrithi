import os
import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

game_catalog = [
    {
        "id": "pic_match",
        "title": "Picture Match",
        "description": "Find and match pairs of familiar household items and fruits.",
        "category": "Visual Memory",
        "t_ref": 15.0
    },
    {
        "id": "face_recall",
        "title": "Face-Name Recall",
        "description": "Recognize family members and match their names correctly.",
        "category": "Facial Recognition",
        "t_ref": 12.0
    },
    {
        "id": "word_find",
        "title": "Word Finding",
        "description": "Identify everyday words in native language from audio prompt.",
        "category": "Language & Recall",
        "t_ref": 10.0
    },
    {
        "id": "sequencing",
        "title": "Daily Task Sequencing",
        "description": "Put morning routine steps in chronological order.",
        "category": "Executive Function",
        "t_ref": 20.0
    }
]

patient_profiles = {
    "patient1": {
        "current_level": 2,
        "history": []
    }
}

game_metrics = {
    "total_sessions": 0,
    "level_ups": 0,
    "level_downs": 0
}

def logistic_probability(level, patient_skill):
    diff = patient_skill - level
    return 1.0 / (1.0 + math.exp(-diff))

def evaluate_adaptive_engine(correct, total, time_taken, t_ref, current_level):
    if total <= 0:
        a = 0.0
    else:
        a = float(correct) / float(total)

    if time_taken <= 0:
        s = 1.0
    else:
        s = min(1.0, float(t_ref) / float(time_taken))

    P = round(0.7 * a + 0.3 * s, 4)

    if P >= 0.80:
        next_level = min(5, current_level + 1)
        action = "LEVEL_UP"
    elif P < 0.50:
        next_level = max(1, current_level - 1)
        action = "LEVEL_DOWN"
    else:
        next_level = current_level
        action = "STAY"

    candidate_levels = [max(1, current_level - 1), current_level, min(5, current_level + 1)]
    patient_skill = current_level + (P - 0.75)
    best_level = min(candidate_levels, key=lambda lvl: abs(logistic_probability(lvl, patient_skill) - 0.75))

    return {
        "accuracy": a,
        "speed_score": s,
        "performance_P": P,
        "action": action,
        "next_level": next_level,
        "recommended_level_target_75": best_level
    }

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"service": "game-service", "status": "UP", "port": 5001}), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    return jsonify(game_metrics), 200

@app.route("/api/games", methods=["GET"])
def get_games():
    patient_id = request.args.get("patient_id", "patient1")
    profile = patient_profiles.setdefault(patient_id, {"current_level": 1, "history": []})
    return jsonify({
        "games": game_catalog,
        "patient_id": patient_id,
        "current_level": profile["current_level"]
    }), 200

@app.route("/api/session/submit", methods=["POST"])
def submit_session():
    data = request.get_json() or {}
    patient_id = data.get("patient_id", "patient1")
    game_id = data.get("game_id", "pic_match")
    correct = int(data.get("correct", 0))
    total = int(data.get("total", 1))
    time_taken = float(data.get("time_taken", 15.0))

    game_item = next((g for g in game_catalog if g["id"] == game_id), game_catalog[0])
    t_ref = game_item["t_ref"]

    profile = patient_profiles.setdefault(patient_id, {"current_level": 1, "history": []})
    current_level = profile["current_level"]

    eval_result = evaluate_adaptive_engine(correct, total, time_taken, t_ref, current_level)

    profile["current_level"] = eval_result["next_level"]
    session_record = {
        "game_id": game_id,
        "correct": correct,
        "total": total,
        "time_taken": time_taken,
        "performance_P": eval_result["performance_P"],
        "level_before": current_level,
        "level_after": eval_result["next_level"],
        "action": eval_result["action"]
    }
    profile["history"].append(session_record)

    game_metrics["total_sessions"] += 1
    if eval_result["action"] == "LEVEL_UP":
        game_metrics["level_ups"] += 1
    elif eval_result["action"] == "LEVEL_DOWN":
        game_metrics["level_downs"] += 1

    return jsonify({
        "status": "success",
        "result": eval_result,
        "history_count": len(profile["history"])
    }), 200

@app.route("/api/history/<patient_id>", methods=["GET"])
def get_history(patient_id):
    profile = patient_profiles.get(patient_id, {"current_level": 1, "history": []})
    return jsonify({
        "patient_id": patient_id,
        "current_level": profile["current_level"],
        "history": profile["history"]
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
