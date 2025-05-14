import sqlite3
import json
from contextlib import closing

DB_PATH = "feedback.db"

def init_feedback_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                campaign_type TEXT,
                product TEXT,
                offer TEXT,
                feedback TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_feedback(user, campaign_type, product, offer, feedback):
    feedback_json = json.dumps(feedback)  # This ensures double quotes!
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO feedback (user, campaign_type, product, offer, feedback)
            VALUES (?, ?, ?, ?, ?)
        """, (user, campaign_type, product, offer, feedback_json))
        conn.commit()


def get_feedback_for_product(product):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT feedback FROM feedback
            WHERE product = ?
        """, (product,))
        # Parse JSON string back to dict
        return [json.loads(row[0]) for row in c.fetchall()]

def get_all_feedback():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT id, user, campaign_type, product, offer, feedback, timestamp FROM feedback
        """)
        rows = c.fetchall()
        # Return as list of dicts, feedback parsed as JSON
        return [
            {
                "id": row[0],
                "user": row[1],
                "campaign_type": row[2],
                "product": row[3],
                "offer": row[4],
                "feedback": json.loads(row[5]),
                "timestamp": row[6]
            }
            for row in rows
        ]

def get_feedback_rating_counts():
    # Example for SQLite; adjust for your DB
    import sqlite3
    conn = sqlite3.connect("feedback.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rating, COUNT(*) FROM feedback GROUP BY rating")
    results = cursor.fetchall()
    conn.close()
    return dict(results)
