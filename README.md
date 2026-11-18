# SupportPilot 🎫
### AI-Powered IT Helpdesk Ticket Classification and Prioritization System

SupportPilot is an AI-powered IT helpdesk system designed to automatically classify support tickets, predict their severity, and assign priority levels. It aims to simplify ticket management and help IT support teams identify and address important issues efficiently.

## 🚀 Project Overview

When an employee submits an IT support ticket, SupportPilot analyzes the ticket description and generates:

- **Category:** Identifies the type of IT issue.
- **Severity:** Predicts how serious the issue is.
- **Priority:** Assigns an appropriate priority level.
- **Confidence:** Displays the model's prediction confidence.
- **Ticket Storage:** Stores ticket information for future reference.

## ✨ Key Features

- Automated IT ticket classification using Machine Learning.
- TF-IDF text vectorization.
- Logistic Regression classification model.
- Severity prediction.
- Priority assignment based on ticket severity and business impact.
- SQLite database integration.
- Flask-based backend.
- Simple web interface for ticket submission and results.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data handling and preprocessing |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning |
| TF-IDF | Text feature extraction |
| Logistic Regression | Ticket classification |
| Flask | Backend and API integration |
| SQLite | Database management |
| HTML & CSS | Frontend interface |
| Jupyter Notebook | Data cleaning and exploration |

## ⚙️ System Workflow

1. **Dataset Collection:** Collect IT support ticket data.
2. **Data Cleaning:** Remove duplicates, handle missing values and prepare the dataset.
3. **Model Training:** Convert ticket descriptions into numerical features using TF-IDF and train a Logistic Regression model.
4. **Ticket Classification:** Predict the category of a newly submitted ticket.
5. **Severity Prediction:** Determine the severity of the issue.
6. **Priority Assignment:** Assign a priority level based on severity and business impact.
7. **Database Storage:** Store ticket details using SQLite.
8. **Web Integration:** Connect the machine learning functionality with the Flask backend and web interface.

## 📂 Project Structure

```text
SupportPilot/
│
├── app.py
├── classifier.py
├── database.py
├── train_model.py
├── data cleaning.ipynb
│
├── templates/
│   └── index.html
│
├── ticket_classifier_model.pkl
├── ticket_vectorizer.pkl
├── requirements.txt
├── .gitignore
└── README.md
```

## 💻 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/snehapriyachavan2108/SupportPilot.git
```

### 2. Navigate to the project directory

```bash
cd SupportPilot
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

Open the local URL displayed in your terminal to access the application.

## 🧠 Machine Learning Approach

SupportPilot uses **TF-IDF (Term Frequency–Inverse Document Frequency)** to transform textual ticket descriptions into numerical features.

A **Logistic Regression** classifier is trained on these features to predict the appropriate IT support ticket category.

The trained model and vectorizer are saved as `.pkl` files for reuse during prediction.

## 📌 Project Status

**Milestone 1 – Completed**

- Dataset collection and preparation.
- Data cleaning and preprocessing.
- Machine Learning model training.
- Ticket category classification.
- Severity and priority prediction.
- Flask integration and web interface.
- Database integration.

*Further improvements and enhancements may be added in future milestones.*

## 🔮 Future Enhancements

- Improved classification accuracy with a larger and more diverse dataset.
- Advanced ticket analytics and dashboard.
- AI-powered ticket resolution suggestions.
- Automated ticket assignment.
- User authentication and role-based access.
- Deployment to a cloud platform.

## 👩‍💻 Author

**Sneha Priya C.**

BE – Computer Science and Engineering (AI & ML)

GitHub: [@snehapriyachavan2108](https://github.com/snehapriyachavan2108)

---

⭐ If you find this project interesting, feel free to explore the repository!
