from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegisterResponse(BaseModel):
    email: EmailStr
    message: str

class LoginResponse(BaseModel):
    email: EmailStr
    message: str

class UserOut(BaseModel):
    id: str
    email: str
