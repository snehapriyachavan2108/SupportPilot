import os
import pickle
import pandas as pd
data = {
    "ticket": 
        ["WiFi is not working",        
         "Internet connection is very slow",        
         "VPN is not connecting",        
         "Unable to access company VPN",        
         "I forgot my password",        
         "Please reset my password",        
         "Install Microsoft Office",        
         "Application installation required",        
         "Laptop keyboard is not working",        
         "Monitor display is not working",
         "Operating system is not booting",
         "Windows update is failing" ],   
         
    "category": [        
             "Network",        
             "Network",        
             "VPN",        
             "VPN",        
             "Password",        
             "Password",        
             "Software",        
             "Software",        
             "Hardware",        
             "Hardware",    
             "System",
             "System"] } 

print("Number of tickets:", len(data["ticket"]))
print("Number of categories:", len(data["category"]))

df = pd.DataFrame(data) 

print(df)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

X = df["ticket"]
y = df["category"]

vectorizer = TfidfVectorizer()
X_vector = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vector, y)

print("Model training completed!")

# Ensure models directory exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

# Save to models/ directory
model_path = os.path.join(MODELS_DIR, "ticket_classifier_model.pkl")
vectorizer_path = os.path.join(MODELS_DIR, "ticket_vectorizer.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

with open(vectorizer_path, "wb") as f:
    pickle.dump(vectorizer, f)

# Also save to root directory for backward compatibility
with open(os.path.join(BASE_DIR, "ticket_classifier_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(BASE_DIR, "ticket_vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print(f"Model and vectorizer saved successfully to {MODELS_DIR} and root!")

