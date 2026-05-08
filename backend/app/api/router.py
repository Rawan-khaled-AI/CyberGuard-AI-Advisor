from fastapi import APIRouter
from app.api.v1 import chat, password, url, email, reports

api_router = APIRouter()

api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(password.router, prefix="/password", tags=["Password"])
api_router.include_router(url.router, prefix="/url", tags=["URL"])
api_router.include_router(email.router, prefix="/email", tags=["Email"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])