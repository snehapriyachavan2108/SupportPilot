import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "supportpilot.db")


def get_db_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the tickets table if it does not already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT,
            email TEXT,
            title TEXT,
            description TEXT,
            category TEXT,
            severity TEXT,
            priority TEXT,
            confidence REAL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def insert_ticket(employee_name, email, title, description, category, severity, priority, confidence, status="Open"):
    """Insert a new ticket into the SQLite database and return its ticket_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tickets (employee_name, email, title, description, category, severity, priority, confidence, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (employee_name, email, title, description, category, severity, priority, confidence, status))
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ticket_id


def get_all_tickets(limit=50):
    """Retrieve the most recent tickets from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY ticket_id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_ticket_by_id(ticket_id):
    """Retrieve a single ticket by its ticket_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_ticket_status(ticket_id, status):
    """Update the status of a ticket (e.g. Open, In progress, Resolved)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (status, ticket_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def get_ticket_stats():
    """Calculate summary statistics and category distribution for the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) AS total FROM tickets")
    total = cursor.fetchone()["total"]
    
    cursor.execute("SELECT COUNT(*) AS open_count FROM tickets WHERE status = 'Open'")
    open_count = cursor.fetchone()["open_count"]
    
    cursor.execute("SELECT COUNT(*) AS resolved_count FROM tickets WHERE status = 'Resolved'")
    resolved_count = cursor.fetchone()["resolved_count"]
    
    cursor.execute("SELECT COUNT(*) AS in_progress_count FROM tickets WHERE status = 'In progress'")
    in_progress_count = cursor.fetchone()["in_progress_count"]
    
    cursor.execute("SELECT COUNT(*) AS high_priority_count FROM tickets WHERE priority IN ('P1', 'P2') AND status != 'Resolved'")
    high_priority_count = cursor.fetchone()["high_priority_count"]
    
    cursor.execute("SELECT category, COUNT(*) as count FROM tickets GROUP BY category")
    category_counts = {row["category"]: row["count"] for row in cursor.fetchall()}
    
    conn.close()
    return {
        "total": total,
        "open": open_count,
        "resolved": resolved_count,
        "in_progress": in_progress_count,
        "high_priority": high_priority_count,
        "category_counts": category_counts
    }


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
