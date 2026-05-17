from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from schema.form_submission import LeadInput
from services.web_scraper import scrape_company_data
from services.wikipedia_retriver import search_company_name
from services.llm_pipeline import llm_report
from services.pdf_report import generate_pdf
from services.email import send_email
from services.bonus import log_to_sheets, upload_to_drive

app = FastAPI()

# Allowing cross communication for * only
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

template = Jinja2Templates(directory='templates')

@app.get('/')
def home(request: Request):
    return template.TemplateResponse('index.html',{'request':request})

# So many request/response only for readability
@app.post('/submit-lead')
def submit_lead(lead : LeadInput):
    try:
        res1 = scrape_company_data(lead.url) 
        res2 = search_company_name(lead.company)
        res3 = llm_report(res1['text'], res2['text'])

        report = res3['report']

        pdf_result = generate_pdf(lead, report)

        _ = send_email(
            to=lead.email,
            name=lead.name,
            company=lead.company,
            pdf_path=pdf_result['report']
        )

        log_to_sheets(lead, report, pdf_result['path'])

        drive_url = upload_to_drive(pdf_result['path'])

        return {
            'success': True,
            'message': f'Email send to {lead.email}',
            'drive_url': drive_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))