import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

model_path = os.path.join(MODELS_DIR, "ticket_classifier_model.pkl")
if not os.path.exists(model_path):
    model_path = os.path.join(BASE_DIR, "ticket_classifier_model.pkl")

vectorizer_path = os.path.join(MODELS_DIR, "ticket_vectorizer.pkl")
if not os.path.exists(vectorizer_path):
    vectorizer_path = os.path.join(BASE_DIR, "ticket_vectorizer.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

#severity prediction

def predict_severity(ticket):    
    text = ticket.lower()    
    critical_words = [        
        "server down",        
        "entire company",        
        "production down",        
        "security breach" ]    
    
    high_words = [        
        "urgent",        
        "cannot work",        
        "business stopped",       
        "client meeting",       
        "vpn not working"    ]    
    
    medium_words = [        
        "slow",        
        "error",        
        "problem",        
        "issue"  ]    
    
    for word in critical_words:        
        if word in text:            
            return "Critical"    
    for word in high_words:        
        if word in text:            
            return "High"    
    for word in medium_words:        
        if word in text:            
            return "Medium"    
    return "Low"


#priority prediction

def calculate_priority(severity, business_impact):    
    if severity == "Critical" and business_impact == "High":        
        return "P1"    
    elif severity == "High" and business_impact == "High":        
        return "P1"    
    elif severity == "High":        
        return "P2"    
    elif severity == "Medium":        
        return "P3"   
    else:        
        return "P4"


def process_ticket(ticket):

    # Category prediction
    ticket_vector = vectorizer.transform([ticket])
    category = model.predict(ticket_vector)[0]

    # Prediction confidence
    confidence = round(float(max(model.predict_proba(ticket_vector)[0]) * 100), 2)

    # Severity prediction
    severity = predict_severity(ticket)

    # Temporary business impact
    business_impact = "High"

    # Priority prediction
    priority = calculate_priority(severity, business_impact)

    return category, severity, priority, confidence


if __name__ == "__main__":
    test_tickets = [
        ("Office WiFi keeps disconnecting", "Network"),
        ("Internet connection is extremely slow", "Network"),
        ("Unable to connect to company VPN", "VPN"),
        ("VPN access is not working", "VPN"),
        ("I forgot my login password", "Password"),
        ("Please reset my account password", "Password"),
        ("Need to install Google Chrome", "Software"),
        ("Laptop keyboard keys are not responding", "Hardware"),
        ("My computer is not booting", "System"),
        ("Windows update installation failed", "System")
    ]

    correct = 0

    severity_scores = {
        "Critical": 4,
        "High": 3,
        "Medium": 2,
        "Low": 1
    }

    print("========== RUNNING TICKET CLASSIFICATION TESTS ==========")

    for ticket, expected_category in test_tickets:
        category, severity, priority, confidence = process_ticket(ticket)
        severity_score = severity_scores[severity]

        if category == expected_category:
            correct += 1

        print("\nTicket:", ticket)
        print("Expected Category:", expected_category)
        print("Predicted Category:", category)
        print("Prediction Confidence:", confidence, "%")
        print("Severity:", severity)
        print("Severity Score:", severity_score, "/ 4")
        print("Priority:", priority)

    accuracy = (correct / len(test_tickets)) * 100

    print("\n========== TEST RESULTS ==========")
    print("Total Tickets:", len(test_tickets))
    print("Correct Predictions:", correct)
    print("Incorrect Predictions:", len(test_tickets) - correct)
    print("Test Accuracy:", round(accuracy, 2), "%")

