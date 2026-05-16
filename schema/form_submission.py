from pydantic import BaseModel, EmailStr

class LeadInput(BaseModel):
    name: str
    email: EmailStr
    company: str
    role: str
    link: str