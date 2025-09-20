from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserRegister(UserBase):
    password: str
    
class UserLogin(UserBase):
    password: str

class UserRegisterResponse(UserBase):
    message: str

class LoginResponse(UserBase):
    message: str

class UserOut(UserBase):
    id: str
