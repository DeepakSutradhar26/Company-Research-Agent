from pydantic import BaseModel, Field
from typing import Optional, Literal

class CompanyIntelligence(BaseModel):
    company_name: str
    website: Optional[str] = Field(description='company websites url')
    industry: Optional[str] = Field(description='which domain does the industry lies')
    founded: Optional[str]
    headquarters: Optional[str] = None
    description: Optional[str] = None
    key_services: Optional[list[str]] = None
    target_market: Optional[str] = None
    company_size: Optional[str] = None

class AuditInsights(BaseModel):
    executive_summary: str = Field(description='2-3 line summary')           
    strengths: list[str]           
    potential_gaps: list[str] = Field(description='How SimplifIQ can help them')        
    recommended_solutions: list[str]

# Pydantic for output parser
class LeadResponse(BaseModel):
    intelligence: CompanyIntelligence
    audut: AuditInsights
    report_status: Literal['generated', 'failed', 'partial'] = 'generated'
    pdf_path: Optional[str] = None
    drive_url: Optional[str] = None
    sheets_logged: Optional[bool] = None 