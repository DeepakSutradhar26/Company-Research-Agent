from pydantic import BaseModel, Field
from typing import Optional, Literal

class CompanyIntelligence(BaseModel):
    company_name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    founded: Optional[str] = None
    headquarters: Optional[str] = None
    description: Optional[str] = None
    key_services: Optional[list[str]] = None
    target_market: Optional[str] = None
    company_size: Optional[str] = None
    business_model: Optional[str] = Field(None, description='B2B, B2C, SaaS, marketplace etc')
    notable_products: Optional[list[str]] = None

class AuditInsights(BaseModel):
    executive_summary: str = Field(description='2-3 line summary of the company and their current position')
    strengths: list[str] = Field(description='Current competitive advantages and what they do well')
    potential_gaps: list[str] = Field(description='Specific operational or strategic gaps where AI automation could help')
    simplifiq_recommendations: list[str] = Field(description='Concrete ways SimplifIQ AI solutions can address their gaps')
    growth_opportunities: list[str] = Field(description='Market or product opportunities the company could pursue')

# Pydantic for output parser
class LeadResponse(BaseModel):
    intelligence: CompanyIntelligence
    audit: AuditInsights
    report_status: Literal['generated', 'failed', 'partial'] = 'generated'
    pdf_path: Optional[str] = None
    drive_url: Optional[str] = None
    sheets_logged: Optional[bool] = None 