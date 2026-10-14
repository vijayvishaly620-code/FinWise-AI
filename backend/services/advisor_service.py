class RuleBasedAdvisor:
    def __init__(self):
        self.rules = []

    def generate_advice(self, user_data):
        advice = []
        income = user_data.get("monthlyIncome", 0) or user_data.get("totalIncome", 0)
        expenses = user_data.get("totalExpenses", 0)
        balance = user_data.get("balance", 0)
        savings_rate = user_data.get("savingsRate", 0)
        categories = user_data.get("categories", {})
        budgets = user_data.get("budgets", [])
        goals = user_data.get("savingsGoals", [])

        if income > 0:
            expense_ratio = (expenses / income) * 100
            if expense_ratio > 90:
                advice.append({"type": "critical", "title": "High Expense Ratio", "message": f"You are spending {expense_ratio:.0f}% of your income. Try to reduce expenses to save more.", "icon": "alert-triangle"})
            elif expense_ratio > 70:
                advice.append({"type": "warning", "title": "Expense Ratio Notice", "message": f"Your expense ratio is {expense_ratio:.0f}%. Consider cutting discretionary spending.", "icon": "alert-circle"})
            elif expense_ratio < 50:
                advice.append({"type": "positive", "title": "Great Expense Control", "message": f"Your expense ratio is only {expense_ratio:.0f}%. Keep up the good work!", "icon": "check-circle"})

        if savings_rate < 10 and income > 0:
            advice.append({"type": "warning", "title": "Low Savings Rate", "message": f"Your savings rate is {savings_rate:.1f}%. Aim for at least 10-20% of your income.", "icon": "trending-down"})
        elif savings_rate >= 20:
            advice.append({"type": "positive", "title": "Excellent Savings Rate", "message": f"Your savings rate is {savings_rate:.1f}%. You are building wealth effectively!", "icon": "trending-up"})

        if income > 0:
            for cat, amount in categories.items():
                pct = (amount / income) * 100
                if cat == "Food" and pct > 20:
                    advice.append({"type": "warning", "title": "High Food Spending", "message": f"Food expenses are {pct:.0f}% of your income. Consider meal planning to reduce costs.", "icon": "utensils"})
                elif cat == "Shopping" and pct > 15:
                    advice.append({"type": "warning", "title": "High Shopping Spending", "message": f"Shopping expenses are {pct:.0f}% of your income. Review discretionary purchases.", "icon": "shopping-bag"})
                elif cat == "Entertainment" and pct > 10:
                    advice.append({"type": "info", "title": "Entertainment Spending", "message": f"Entertainment is {pct:.0f}% of income. Look for free or low-cost alternatives.", "icon": "film"})

        for budget in budgets:
            spent = budget.get("spent", 0)
            amount = budget.get("budgetAmount", 0)
            if amount > 0:
                pct = (spent / amount) * 100
                if pct >= 100:
                    advice.append({"type": "critical", "title": f"{budget['category']} Budget Exceeded", "message": f"Your {budget['category']} budget has been exceeded by {spent - amount:.0f}.", "icon": "alert-triangle"})
                elif pct >= 90:
                    advice.append({"type": "warning", "title": f"{budget['category']} Budget Critical", "message": f"Your {budget['category']} budget is {pct:.0f}% used. Only {amount - spent:.0f} remaining.", "icon": "alert-circle"})

        for goal in goals:
            progress = (goal.get("currentAmount", 0) / goal.get("targetAmount", 1)) * 100
            if progress >= 100:
                advice.append({"type": "positive", "title": f"Goal Achieved: {goal['goalName']}", "message": f"Congratulations! You have reached your savings goal for {goal['goalName']}.", "icon": "star"})
            elif progress >= 50:
                advice.append({"type": "info", "title": f"Goal Progress: {goal['goalName']}", "message": f"You are {progress:.0f}% towards your {goal['goalName']} goal. Keep saving!", "icon": "target"})

        if not advice:
            advice.append({"type": "info", "title": "Getting Started", "message": "Add more financial data to receive personalized advice.", "icon": "info"})

        return advice

    def chat_response(self, message, user_data):
        message = message.lower()
        income = user_data.get("monthlyIncome", 0) or user_data.get("totalIncome", 0)
        expenses = user_data.get("totalExpenses", 0)
        balance = user_data.get("balance", 0)
        savings_rate = user_data.get("savingsRate", 0)
        categories = user_data.get("categories", {})
        goals = user_data.get("savingsGoals", [])

        if any(w in message for w in ["save", "saving", "savings"]):
            if goals:
                goal_info = ", ".join([f"{g['goalName']} ({g.get('currentAmount', 0)}/{g['targetAmount']})" for g in goals[:3]])
                return f"Your current savings goals are: {goal_info}. "
            target = income * 0.2 if income > 0 else 0
            return f"Based on your income of {income:.0f}, try to save at least {target:.0f} per month (20%). Your current savings rate is {savings_rate:.1f}%."

        if any(w in message for w in ["overspend", "overspending", "spending too much", "too much"]):
            if expenses > income and income > 0:
                return f"You are currently spending more than you earn. Your expenses ({expenses:.0f}) exceed your income ({income:.0f}) by {expenses - income:.0f}. Focus on reducing non-essential spending."
            expense_ratio = (expenses / income * 100) if income > 0 else 0
            if expense_ratio > 70:
                return f"Your expense ratio is {expense_ratio:.0f}%, which is on the higher side. Review your top spending categories and look for areas to cut back."
            return f"Your spending looks reasonable with an expense ratio of {expense_ratio:.0f}%. Keep monitoring your expenses regularly."

        if any(w in message for w in ["budget", "budgeting"]):
            budgets = user_data.get("budgets", [])
            if budgets:
                over = [b for b in budgets if b.get("percentage", 0) >= 90]
                if over:
                    names = ", ".join([b["category"] for b in over])
                    return f"Your {names} budget(s) are at 90% or above. Consider reducing spending in these areas."
                return "Your budgets are looking good! All categories are within acceptable limits."
            return "You haven't set up budgets yet. Go to the Budget page to create monthly budgets for each expense category."

        if any(w in message for w in ["invest", "investment"]):
            if savings_rate >= 20:
                return f"With a savings rate of {savings_rate:.1f}%, you are in a good position to start investing. Consider diversifying into index funds, mutual funds, or fixed deposits. (Note: This is educational advice, not guaranteed returns.)"
            return f"Focus on building your savings first. Your current savings rate is {savings_rate:.1f}%. Aim for at least 20% before investing."

        if any(w in message for w in ["how much", "should i save", "target"]):
            if income > 0:
                targets = {
                    "conservative": income * 0.1,
                    "moderate": income * 0.2,
                    "aggressive": income * 0.3,
                }
                return f"Based on your income of {income:.0f}: Conservative target: {targets['conservative']:.0f}/month (10%). Moderate target: {targets['moderate']:.0f}/month (20%). Aggressive target: {targets['aggressive']:.0f}/month (30%)."
            return "Please add your income information so I can calculate savings targets for you."

        if any(w in message for w in ["hello", "hi", "hey"]):
            return f"Hello! I'm your FinWise AI advisor. I can help you with budgeting, saving, and understanding your financial health. Your current balance is {balance:.0f}. What would you like to know?"

        if any(w in message for w in ["health", "score", "financial health"]):
            return f"Your savings rate is {savings_rate:.1f}% and your expense ratio is {(expenses/income*100) if income > 0 else 0:.1f}%. Check the AI Advisor page for your full financial health score."

        top_cat = max(categories, key=categories.get) if categories else None
        if top_cat:
            return f"Your largest expense category is {top_cat} at {categories[top_cat]:.0f}. Your total expenses are {expenses:.0f} against an income of {income:.0f}. How can I help you manage your finances better?"
        return "I can help you with budgeting, saving tips, expense analysis, and financial health. What would you like to know?"
