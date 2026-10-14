from datetime import datetime
from models.transaction_model import TransactionModel
from models.budget_model import BudgetModel
from models.savings_model import SavingsModel
from models.alert_model import AlertModel


def calculate_financial_health_score(db, user_id):
    tx_model = TransactionModel(db)
    budget_model = BudgetModel(db)
    savings_model = SavingsModel(db)
    now = datetime.now()
    summary = tx_model.get_summary(user_id, str(now.month), str(now.year))
    budgets = budget_model.get_all(user_id, f"{now.year}-{now.month:02d}")
    goals = savings_model.get_all(user_id)
    score = 50
    if summary["income"] > 0:
        savings_rate = (summary["balance"] / summary["income"]) * 100
        if savings_rate >= 20:
            score += 25
        elif savings_rate >= 10:
            score += 15
        elif savings_rate >= 5:
            score += 5
        else:
            score -= 10
        expense_ratio = (summary["expense"] / summary["income"]) * 100
        if expense_ratio <= 50:
            score += 15
        elif expense_ratio <= 70:
            score += 10
        elif expense_ratio <= 80:
            score += 0
        else:
            score -= 10
    if budgets:
        within_budget = sum(1 for b in budgets if b.get("percentage", 0) <= 100)
        budget_score = (within_budget / len(budgets)) * 10
        score += int(budget_score)
    if goals:
        avg_progress = sum(min(g.get("currentAmount", 0) / max(g.get("targetAmount", 1), 1), 1) for g in goals) / len(goals)
        score += int(avg_progress * 10)
    score = max(0, min(100, score))
    return score


def get_health_label(score):
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Needs Improvement"
    else:
        return "Poor"


def generate_alerts_for_transactions(db, user_id):
    alert_model = AlertModel(db)
    tx_model = TransactionModel(db)
    budget_model = BudgetModel(db)
    now = datetime.now()
    month_str = f"{now.year}-{now.month:02d}"
    summary = tx_model.get_summary(user_id, str(now.month), str(now.year))
    budgets = budget_model.get_all(user_id, month_str)
    categories = tx_model.get_category_summary(user_id, str(now.month), str(now.year))
    cat_map = {c["_id"]: c["total"] for c in categories}
    for budget in budgets:
        spent = cat_map.get(budget["category"], 0)
        amount = budget["budgetAmount"]
        pct = (spent / amount * 100) if amount > 0 else 0
        if pct >= 100:
            alert_model.create(user_id, {
                "type": "critical",
                "title": f"{budget['category']} Budget Exceeded",
                "message": f"Your {budget['category']} budget of {amount:.0f} has been exceeded. Current spending: {spent:.0f}."
            })
        elif pct >= 90:
            alert_model.create(user_id, {
                "type": "warning",
                "title": f"{budget['category']} Budget Critical",
                "message": f"Your {budget['category']} budget is {pct:.0f}% used. Only {amount - spent:.0f} remaining."
            })
        elif pct >= 70:
            alert_model.create(user_id, {
                "type": "info",
                "title": f"{budget['category']} Budget Warning",
                "message": f"Your {budget['category']} budget is {pct:.0f}% used."
            })
    if summary["income"] > 0:
        savings_rate = (summary["balance"] / summary["income"]) * 100
        if savings_rate > 20:
            alert_model.create(user_id, {
                "type": "positive",
                "title": "Great Savings!",
                "message": f"You saved {savings_rate:.1f}% of your income this month. Keep it up!"
            })
    goals = SavingsModel(db).get_all(user_id)
    for goal in goals:
        progress = (goal.get("currentAmount", 0) / goal.get("targetAmount", 1)) * 100
        if progress >= 100:
            alert_model.create(user_id, {
                "type": "positive",
                "title": f"Goal Achieved: {goal['goalName']}",
                "message": f"Congratulations! You have reached your savings goal for {goal['goalName']}!"
            })
        elif progress >= 50:
            alert_model.create(user_id, {
                "type": "info",
                "title": f"Halfway to {goal['goalName']}",
                "message": f"You have reached 50% of your {goal['goalName']} savings goal!"
            })
