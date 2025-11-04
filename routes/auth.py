from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.supabase_client import DatabaseHandler

supabase = DatabaseHandler()

router = APIRouter(prefix="/auth", tags=["Auth"])

class AuthSchema(BaseModel):
    name: str = Field("Zohaib Munir")
    email: str = Field("zohaibmunir32@gmail.com")
    password: str = Field("aaaaaa")
    phone_number: str = Field("+923364359237", alias="phone")

@router.post("/register")
def register_user(auth: AuthSchema):
    try:
        return supabase.register_user(auth.name, auth.email, auth.password, auth.phone_number)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(auth: AuthSchema):
    try:
        return supabase.login_user(auth.email, auth.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users")
def get_all_users():
    try:
        return supabase.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
