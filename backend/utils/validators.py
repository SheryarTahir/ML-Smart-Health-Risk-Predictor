import re
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate_register(d):
    if not d.get("name") or len(d["name"]) < 2:
        return "Name must be at least 2 characters"
    if not d.get("email") or not EMAIL_RE.match(d["email"]):
        return "Invalid email"
    if not d.get("password") or len(d["password"]) < 6:
        return "Password must be at least 6 characters"
    return None

def validate_login(d):
    if not d.get("email") or not EMAIL_RE.match(d["email"]):
        return "Invalid email"
    if not d.get("password"):
        return "Password required"
    return None
