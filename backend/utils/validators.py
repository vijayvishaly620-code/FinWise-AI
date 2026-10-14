import re


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Valid"


def validate_amount(amount):
    try:
        val = float(amount)
        return val > 0, "Amount must be positive"
    except (ValueError, TypeError):
        return False, "Invalid amount"


def validate_transaction(data):
    errors = []
    if not data.get("type") or data["type"] not in ["income", "expense"]:
        errors.append("Type must be 'income' or 'expense'")
    valid, msg = validate_amount(data.get("amount"))
    if not valid:
        errors.append(msg)
    if data.get("type") == "expense" and not data.get("category"):
        errors.append("Category is required for expenses")
    return len(errors) == 0, errors


def sanitize_input(text):
    if not text:
        return text
    return text.strip()
