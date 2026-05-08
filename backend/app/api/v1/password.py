from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PasswordRequest(BaseModel):
    password: str

@router.post("/check")
def check_password(data: PasswordRequest):
    password = data.password

    score = 0

    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*" for c in password):
        score += 1

    if score <= 1:
        strength = "Weak"
    elif score == 2:
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "strength": strength,
        "score": score
    }