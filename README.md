# FinWise AI – Personal Finance Advisor

A full-stack AI-powered personal finance application built with React, Flask, MongoDB, and Scikit-learn.

## Features

- **Authentication** – Register, Login, JWT-based auth, profile management
- **Income & Expense Tracking** – Full CRUD with search, filter, sort
- **Budget Management** – Category budgets with progress bars and alerts
- **Savings Goals** – Track goals with progress and required monthly savings
- **AI Advisor** – Rule-based + ML financial health analysis
- **Finance Chatbot** – Ask questions about your finances
- **Expense Prediction** – ML-based next month expense estimation
- **Dashboard & Analytics** – Charts, trends, financial health score
- **Reports** – Monthly/yearly reports with CSV download
- **Alert System** – Automatic budget and savings alerts
- **Demo Account** – Pre-populated with realistic sample data

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, Vite, React Router, Recharts, Lucide React |
| Backend | Python, Flask, Flask-CORS, PyMongo, JWT |
| Database | MongoDB |
| ML/AI | Scikit-learn, Pandas, NumPy, Joblib |

## Project Structure

```
FinWise-AI/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # Layout, shared components
│   │   ├── pages/         # All page components
│   │   ├── services/      # API service layer
│   │   └── styles/        # CSS styles
│   ├── package.json
│   └── vite.config.js
├── backend/               # Flask backend
│   ├── app.py             # Main Flask app
│   ├── config.py          # Configuration
│   ├── routes/            # API route handlers
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   ├── ml/                # ML training & prediction
│   ├── datasets/          # CSV datasets
│   ├── utils/             # Utility functions
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB (running locally or Atlas URI)

### 1. Clone & Navigate

```bash
cd FinWise-AI
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your MongoDB URI and JWT secret
```

### 3. MongoDB Setup

Make sure MongoDB is running on `localhost:27017` or update `MONGO_URI` in `.env`.

```bash
# If using local MongoDB, just start the service
# Or use MongoDB Atlas and set MONGO_URI in .env
```

### 4. Seed Demo Account

```bash
python seed_demo.py
```

This creates the demo account with sample data:
- Email: `demo@finwise.ai`
- Password: `Demo@123`

### 5. Train ML Models (Optional)

```bash
cd ml
python train_model.py
```

### 6. Start Backend

```bash
cd ..
python app.py
```

Backend runs on `http://localhost:5000`

### 7. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on `http://localhost:3000`

### 8. Open Browser

Navigate to `http://localhost:3000`

## Demo Login

| Field | Value |
|-------|-------|
| Email | demo@finwise.ai |
| Password | Demo@123 |

## API Endpoints

### Authentication
- `POST /api/auth/register` – Register new user
- `POST /api/auth/login` – Login
- `GET /api/auth/profile` – Get profile (protected)
- `PUT /api/auth/profile` – Update profile (protected)

### Transactions
- `GET /api/transactions` – List transactions
- `POST /api/transactions` – Create transaction
- `PUT /api/transactions/:id` – Update transaction
- `DELETE /api/transactions/:id` – Delete transaction

### Budgets
- `GET /api/budgets` – List budgets
- `POST /api/budgets` – Create budget
- `PUT /api/budgets/:id` – Update budget
- `DELETE /api/budgets/:id` – Delete budget

### Savings
- `GET /api/savings` – List savings goals
- `POST /api/savings` – Create goal
- `PUT /api/savings/:id` – Update goal
- `DELETE /api/savings/:id` – Delete goal

### Dashboard
- `GET /api/dashboard/summary` – Financial summary
- `GET /api/dashboard/analytics` – Charts data

### AI Advisor
- `POST /api/advisor/analyze` – Get financial advice
- `POST /api/advisor/chat` – Chat with advisor
- `POST /api/advisor/predict-expenses` – Predict next month
- `GET /api/advisor/financial-health` – Health score

### Reports
- `GET /api/reports/monthly` – Monthly report
- `GET /api/reports/yearly` – Yearly report
- `GET /api/reports/download` – Download CSV

### Alerts
- `GET /api/alerts` – List alerts
- `PUT /api/alerts/:id/read` – Mark as read

## Datasets

Located in `backend/datasets/`:

- `expenses_dataset.csv` – 500+ expense records
- `income_dataset.csv` – 200+ income records
- `budget_dataset.csv` – 300+ budget records
- `financial_behavior_dataset.csv` – 1000 synthetic records for ML training

## Machine Learning

Two ML models are trained:

1. **Financial Health Classifier** (RandomForestClassifier)
   - Features: income, expenses, category spending, savings, debt, budget usage
   - Target: Poor / Average / Good / Excellent

2. **Expense Predictor** (RandomForestRegressor)
   - Features: previous month expenses, rolling averages, category spending
   - Target: Next month total expense

Train models:
```bash
cd backend/ml
python train_model.py
```

## Financial Health Score

Score 0-100 based on:
- Savings rate (20%+ = excellent)
- Budget adherence
- Expense ratio
- Goal progress

| Score | Rating |
|-------|--------|
| 80-100 | Excellent |
| 60-79 | Good |
| 40-59 | Needs Improvement |
| 0-39 | Poor |

## License

This project is for educational purposes.
