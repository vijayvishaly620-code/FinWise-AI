from models.transaction_model import TransactionModel
from models.budget_model import BudgetModel
from models.savings_model import SavingsModel


class FinanceService:
    def __init__(self, db):
        self.db = db
        self.tx_model = TransactionModel(db)
        self.budget_model = BudgetModel(db)
        self.savings_model = SavingsModel(db)

    def get_financial_overview(self, user_id, month=None, year=None):
        summary = self.tx_model.get_summary(user_id, month, year)
        budgets = self.budget_model.get_all(user_id, month)
        goals = self.savings_model.get_all(user_id)
        total_savings_goal = sum(g.get("targetAmount", 0) for g in goals)
        total_saved = sum(g.get("currentAmount", 0) for g in goals)
        return {
            "income": summary["income"],
            "expenses": summary["expense"],
            "balance": summary["balance"],
            "savingsRate": round((summary["balance"] / summary["income"] * 100), 1) if summary["income"] > 0 else 0,
            "expenseRatio": round((summary["expense"] / summary["income"] * 100), 1) if summary["income"] > 0 else 0,
            "budgetsCount": len(budgets),
            "savingsGoalsCount": len(goals),
            "totalSavingsGoal": total_savings_goal,
            "totalSaved": total_saved,
        }

    def compare_months(self, user_id, current_month, current_year, prev_month, prev_year):
        current = self.tx_model.get_summary(user_id, current_month, current_year)
        prev = self.tx_model.get_summary(user_id, prev_month, prev_year)
        income_change = 0
        expense_change = 0
        if prev["income"] > 0:
            income_change = round(((current["income"] - prev["income"]) / prev["income"]) * 100, 1)
        if prev["expense"] > 0:
            expense_change = round(((current["expense"] - prev["expense"]) / prev["expense"]) * 100, 1)
        return {
            "current": current,
            "previous": prev,
            "incomeChange": income_change,
            "expenseChange": expense_change,
        }
