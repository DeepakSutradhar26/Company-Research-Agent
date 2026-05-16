from pydantic import BaseModel, EmailStr

# Pydantic does the validation of form input
class LeadInput(BaseModel):
    name: str
    email: EmailStr
    company: str
    role: str | None = None
    url: str | None = None