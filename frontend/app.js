const GAME_SERVICE_URL = "http://localhost:5001";
const MEMORY_SERVICE_URL = "http://localhost:5002";

let currentPatient = "patient1";
let currentLevel = 1;
let activeGame = null;
let roundStartTime = 0;
let correctClicks = 0;

const defaultGames = [
    {
        id: "pic_match",
        title: "Picture Match",
        category: "Visual Memory",
        description: "Find matching pairs of familiar objects.",
        t_ref: 15.0
    },
    {
        id: "face_recall",
        title: "Face-Name Recall",
        category: "Facial Recognition",
        description: "Recognize family members and their names.",
        t_ref: 12.0
    },
    {
        id: "word_find",
        title: "Word Finding",
        category: "Language & Recall",
        description: "Identify everyday regional words.",
        t_ref: 10.0
    },
    {
        id: "sequencing",
        title: "Daily Task Sequencing",
        category: "Executive Function",
        description: "Organize daily routine steps in order.",
        t_ref: 20.0
    }
];

const defaultReminders = [
    { id: 1, title: "Donepezil 5mg", time: "08:00 AM", type: "Medicine", status: "taken" },
    { id: 2, title: "Morning Walk in Garden", time: "09:30 AM", type: "Routine", status: "completed" },
    { id: 3, title: "Amlodipine 5mg", time: "02:00 PM", type: "Medicine", status: "missed" },
    { id: 4, title: "Call Son Rahul", time: "06:00 PM", type: "Routine", status: "pending" }
];

function switchView(viewName) {
    document.querySelectorAll(".view-section").forEach(sec => sec.classList.remove("active"));
    document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));

    const targetSec = document.getElementById("view-" + viewName);
    if (targetSec) targetSec.classList.add("active");

    const buttons = document.querySelectorAll(".nav-btn");
    buttons.forEach(btn => {
        if (btn.innerText.toLowerCase().includes(viewName.slice(0, 4))) {
            btn.classList.add("active");
        }
    });

    if (viewName === "memory") loadMemoryGraph();
    if (viewName === "caregiver") loadCaregiverAlerts();
}

function speakPrompt(text) {
    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

function renderGames() {
    const container = document.getElementById("games-container");
    container.innerHTML = "";

    defaultGames.forEach(game => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <div>
                <span class="card-badge">${game.category}</span>
                <h3 class="card-title">${game.title}</h3>
                <p class="card-desc">${game.description}</p>
            </div>
            <button class="large-btn" style="font-size: 18px; padding: 10px 18px;" onclick="startGame('${game.id}')">Play Game</button>
        `;
        container.appendChild(card);
    });
}

function startGame(gameId) {
    activeGame = defaultGames.find(g => g.id === gameId);
    if (!activeGame) return;

    document.getElementById("game-active-area").style.display = "block";
    document.getElementById("active-game-title").innerText = activeGame.title;
    document.getElementById("round-feedback").innerText = "";

    const board = document.getElementById("game-tiles");
    board.innerHTML = "";
    correctClicks = 0;
    roundStartTime = Date.now();

    const symbols = ["🍎", "🍵", "🏠", "🌸", "🍎", "🌸"];
    symbols.sort(() => Math.random() - 0.5);

    symbols.forEach(sym => {
        const tile = document.createElement("div");
        tile.className = "interactive-tile";
        tile.innerText = "?";
        tile.onclick = () => {
            tile.innerText = sym;
            tile.style.backgroundColor = "#0284c7";
            correctClicks++;
            speakPrompt(sym);
        };
        board.appendChild(tile);
    });

    speakPrompt("Game started: " + activeGame.title + ". Tap the boxes.");
    window.scrollTo({ top: document.getElementById("game-active-area").offsetTop - 40, behavior: "smooth" });
}

async function finishCurrentRound() {
    const duration = Math.max(1, (Date.now() - roundStartTime) / 1000);
    const correct = Math.min(4, Math.max(1, correctClicks));
    const total = 4;

    const a = correct / total;
    const s = Math.min(1.0, activeGame.t_ref / duration);
    const P = Number((0.7 * a + 0.3 * s).toFixed(4));

    let action = "STAY";
    if (P >= 0.80) {
        currentLevel = Math.min(5, currentLevel + 1);
        action = "LEVEL UP";
    } else if (P < 0.50) {
        currentLevel = Math.max(1, currentLevel - 1);
        action = "LEVEL DOWN";
    }

    document.getElementById("lbl-level").innerText = currentLevel;

    const feedback = `Round complete! Accuracy: ${(a*100).toFixed(0)}%, Time: ${duration.toFixed(1)}s, Score (P): ${P}. Engine Decision: ${action}`;
    document.getElementById("round-feedback").innerText = feedback;
    speakPrompt(action === "LEVEL UP" ? "Excellent work! Advancing to level " + currentLevel : "Good effort. Let us try again.");

    try {
        await fetch(`${GAME_SERVICE_URL}/api/session/submit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                patient_id: currentPatient,
                game_id: activeGame.id,
                correct: correct,
                total: total,
                time_taken: duration
            })
        });
    } catch (e) {
    }
}

function renderReminders() {
    const container = document.getElementById("reminders-container");
    container.innerHTML = "";

    defaultReminders.forEach(r => {
        const item = document.createElement("div");
        item.className = "reminder-item";
        item.innerHTML = `
            <div>
                <div class="reminder-title">${r.title}</div>
                <div class="reminder-time">Scheduled: ${r.time} (${r.type})</div>
            </div>
            <div style="display: flex; gap: 10px; align-items: center;">
                <span class="status-badge status-${r.status}">${r.status.toUpperCase()}</span>
                <button class="large-btn" style="padding: 8px 12px; font-size: 14px;" onclick="speakPrompt('${r.title} at ${r.time}')">Speak</button>
            </div>
        `;
        container.appendChild(item);
    });
}

async function loadMemoryGraph() {
    const box = document.getElementById("graph-content");
    box.innerHTML = `
        <strong>Patient Node:</strong> Biren Das (Assam, NER)<br>
        <strong>Relationships:</strong><br>
        &bull; [Biren Das] &rarr; HAS_SON &rarr; [Rahul Das] (Lives in Guwahati, Phone: 9876543210)<br>
        &bull; [Biren Das] &rarr; CONSULTS &rarr; [Dr. Barua] (Shillong Civil Hospital)<br>
        &bull; [Biren Das] &rarr; TAKES_MORNING &rarr; [Donepezil 5mg] at 08:00 AM<br>
        &bull; [Biren Das] &rarr; TAKES_AFTERNOON &rarr; [Amlodipine 5mg] at 02:00 PM<br>
    `;

    try {
        const res = await fetch(`${MEMORY_SERVICE_URL}/api/memory-graph/${currentPatient}`);
        const data = await res.json();
        if (data && data.graph && data.graph.relationships) {
            let html = `<strong>Patient:</strong> ${data.patient_id}<br><strong>Relationships:</strong><br>`;
            data.graph.relationships.forEach(rel => {
                html += `&bull; [${rel.source}] &rarr; ${rel.edge} &rarr; [${rel.target}]<br>`;
            });
            box.innerHTML = html;
        }
    } catch (e) {
    }
}

async function loadCaregiverAlerts() {
    const container = document.getElementById("caregiver-alerts-container");
    container.innerHTML = `
        <div class="alert-banner">
            WARNING: Patient missed 3 consecutive doses of Amlodipine 5mg (2:00 PM). Automated SMS/Voice alert sent to caregiver Rahul Das.
        </div>
    `;

    try {
        const res = await fetch(`${MEMORY_SERVICE_URL}/api/caregiver/alerts`);
        const data = await res.json();
        if (data.alerts && data.alerts.length > 0) {
            container.innerHTML = "";
            data.alerts.forEach(a => {
                const banner = document.createElement("div");
                banner.className = "alert-banner";
                banner.innerText = `${a.severity}: ${a.message}`;
                container.appendChild(banner);
            });
            document.getElementById("metric-alerts-count").innerText = data.alerts.length;
        }
    } catch (e) {
    }
}

document.addEventListener("DOMContentLoaded", () => {
    renderGames();
    renderReminders();
});
