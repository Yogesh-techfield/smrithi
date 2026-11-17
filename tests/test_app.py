import sys
import os
sys.path.insert(0, os.path.abspath("."))

from services.auth_service.app import app as auth_app
from services.game_service.app import app as game_app, evaluate_adaptive_engine
from services.memory_service.app import app as memory_app, evaluate_caregiver_alerts

def test_auth_health():
    client = auth_app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["status"] == "UP"

def test_auth_login_success():
    client = auth_app.test_client()
    res = client.post("/api/login", json={"username": "patient1", "password": "pass123"})
    assert res.status_code == 200
    assert "token" in res.json

def test_auth_login_invalid():
    client = auth_app.test_client()
    res = client.post("/api/login", json={"username": "patient1", "password": "wrong"})
    assert res.status_code == 401

def test_game_health():
    client = game_app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json["port"] == 5001

def test_adaptive_difficulty_level_up():
    result = evaluate_adaptive_engine(correct=4, total=4, time_taken=10.0, t_ref=15.0, current_level=1)
    assert result["performance_P"] >= 0.80
    assert result["action"] == "LEVEL_UP"
    assert result["next_level"] == 2

def test_adaptive_difficulty_level_down():
    result = evaluate_adaptive_engine(correct=1, total=4, time_taken=30.0, t_ref=10.0, current_level=3)
    assert result["performance_P"] < 0.50
    assert result["action"] == "LEVEL_DOWN"
    assert result["next_level"] == 2

def test_game_session_submit():
    client = game_app.test_client()
    res = client.post("/api/session/submit", json={
        "patient_id": "patient1",
        "game_id": "pic_match",
        "correct": 4,
        "total": 4,
        "time_taken": 12.0
    })
    assert res.status_code == 200
    assert res.json["status"] == "success"

def test_memory_reminders():
    client = memory_app.test_client()
    res = client.get("/api/reminders/patient1")
    assert res.status_code == 200
    assert len(res.json["reminders"]) >= 1

def test_caregiver_alerts_missed_meds():
    alerts = evaluate_caregiver_alerts("patient1", [0.75, 0.74, 0.73])
    types = [a["type"] for a in alerts]
    assert "MISSED_MEDICINE" in types

def test_caregiver_alerts_slope_decline():
    alerts = evaluate_caregiver_alerts("patient1", [0.80, 0.70, 0.60])
    types = [a["type"] for a in alerts]
    assert "COGNITIVE_DECLINE" in types
