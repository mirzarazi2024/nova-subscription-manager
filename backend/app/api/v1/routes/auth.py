from fastapi import APIRouter
from pydantic import BaseModel

from app.security.jwt import create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    role = "admin" if payload.username == "admin" else "user"
    token = create_access_token(subject=payload.username, role=role)
    return LoginResponse(access_token=token)
