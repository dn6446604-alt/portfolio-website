import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

# Portfolio/
# ├── frontend/
# │   ├── index.html
# │   ├── style.css
# │   └── script.js
# └── backend/
#     └── app.py

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
DATABASE = BASE_DIR / "portfolio.db"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT DEFAULT '',
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()


@app.get("/")
def home():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "Portfolio backend is running"
    })


@app.post("/api/contact")
def contact():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    subject = str(data.get("subject", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not email or not message:
        return jsonify({
            "success": False,
            "error": "Name, email and message are required."
        }), 400

    created_at = datetime.now(timezone.utc).isoformat()

    with get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO messages
            (name, email, subject, message, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, email, subject, message, created_at)
        )
        conn.commit()

    return jsonify({
        "success": True,
        "message": "Your message was received.",
        "id": cursor.lastrowid
    }), 201


@app.get("/api/messages")
def messages():
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, name, email, subject, message, created_at
            FROM messages
            ORDER BY id DESC
            """
        ).fetchall()

    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
