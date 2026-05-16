from pydantic import BaseModel, EmailStr

class LeadInput(BaseModel):
    name: str
    email: EmailStr
    company: str
    role: str | None = None
    link: str | None = None