from flask import Flask, request, jsonify, render_template
from classifier import process_ticket 
import database as db

app = Flask(__name__) 

# Ensure SQLite database and tickets table exist on app start
db.init_db()

@app.route("/")
def home():
    """Serve the SupportPilot frontend dashboard."""
    return render_template("index.html")

@app.route("/ticket", methods=["POST"]) 
@app.route("/api/tickets", methods=["POST"])
def create_ticket():    
    data = request.json or {}    
    
    title = data.get("title", "Untitled Ticket")
    description = data.get("description", "")
    email = data.get("email", "")
    employee_name = data.get("employee_name", data.get("department", "Employee"))
    
    if not description:
        return jsonify({"error": "Ticket description is required."}), 400
    
    # 1. AI & rule-based classification
    category, severity, priority, confidence = process_ticket(description)    
    
    # 2. Store ticket into SQLite database
    ticket_id = db.insert_ticket(
        employee_name=employee_name,
        email=email,
        title=title,
        description=description,
        category=category,
        severity=severity,
        priority=priority,
        confidence=confidence,
        status="Open"
    )
    
    # 3. Retrieve stored record
    stored_ticket = db.get_ticket_by_id(ticket_id)
    
    return jsonify({
        "status": "success",
        "ticket_id": ticket_id,
        "category": category,
        "confidence": confidence,
        "severity": severity,
        "priority": priority,
        "ticket": stored_ticket
    }), 201

@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    """Retrieve all tickets from the database."""
    tickets = db.get_all_tickets()
    return jsonify({
        "status": "success",
        "count": len(tickets),
        "tickets": tickets
    })

@app.route("/api/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    """Retrieve details of a single ticket."""
    ticket = db.get_ticket_by_id(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return jsonify({
        "status": "success",
        "ticket": ticket
    })

@app.route("/api/tickets/<int:ticket_id>/status", methods=["POST", "PATCH"])
def update_ticket_status(ticket_id):
    """Update ticket status (Open, In progress, Resolved)."""
    data = request.json or {}
    new_status = data.get("status")
    
    valid_statuses = ["Open", "In progress", "Resolved", "Closed"]
    if not new_status or new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of: {', '.join(valid_statuses)}"}), 400
        
    updated = db.update_ticket_status(ticket_id, new_status)
    if not updated:
        return jsonify({"error": "Ticket not found or status not changed"}), 404
        
    ticket = db.get_ticket_by_id(ticket_id)
    return jsonify({
        "status": "success",
        "ticket_id": ticket_id,
        "new_status": new_status,
        "ticket": ticket
    })

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Retrieve KPI statistics for the dashboard."""
    stats = db.get_ticket_stats()
    return jsonify({
        "status": "success",
        "stats": stats
    })

if __name__ == "__main__":    
    app.run(debug=True)

