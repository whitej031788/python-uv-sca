from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import hashlib
import logging
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.database import user_db

logger = logging.getLogger(__name__)

router = APIRouter()

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str  # Password should be validated for strength

@router.post("/register", response_model=dict)
async def register_user(user_data: UserCreate):
    # No validation on username/password strength
    existing_user = user_db.get_user_by_username(user_data.username)  # cross-file SQL injection (not getting picked up)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    hashed_password = user_data.password
    
    # Inserting user with SQL injection vulnerability
    cursor = user_db.sqlite_conn.cursor()
    query = f"INSERT INTO users (username, password, email) VALUES ('{user_data.username}', '{hashed_password}', '{user_data.email}')"
    cursor.execute(query)  # SQL Injection!
    user_db.sqlite_conn.commit()

    
    return {"message": "User registered successfully", "username": user_data.username}

def canary():
    am_i_being_scanned = "?"
    return