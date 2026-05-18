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
    allow_origins=[
        'https://company-research-agent-production-e45b.up.railway.app',
        'http://127.0.0.1:8000',
        '*'
    ],
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

        scraped_text = res1.get('text', '') if res1.get('success') else ''
        wiki_text = res2.get('text', '') if res2.get('success') else ''

        res3 = llm_report(scraped_text, wiki_text)

        if not res3.get('success'):
            raise Exception(f"Report generation failed: {res3.get('message')}")
        
        report = res3['report']

        pdf_result = generate_pdf(lead, report)

        email_result = send_email(
            to=lead.email,
            name=lead.name,
            company=lead.company,
            pdf_path=pdf_result['path']
        )

        if not email_result.get('success'):
            raise Exception(f"Email failed: {email_result.get('message')}")

        try:
            drive_result = upload_to_drive(pdf_result['path'])
            drive_url = drive_result.get('url', '') if drive_result.get('success') else ''
        except Exception as e:
            print(f'Drive upload skipped: {e}')
            drive_url = ''

        try:
            log_to_sheets(lead, drive_url or pdf_result['path'])
        except Exception as e:
            print(f'Sheets logging skipped: {e}')

        return {
            'success': True,
            'message': f'Email sent to {lead.email}',
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))