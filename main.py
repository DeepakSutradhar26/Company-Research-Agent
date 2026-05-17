from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from schema.form_submission import LeadInput
from services.web_scraper import scrape_company_data
from services.wikipedia_retriver import search_company_name

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

@app.post('/submit-lead')
def submit_lead(lead : LeadInput):
    try:
        res1 = scrape_company_data(lead.url) 
        res2 = search_company_name(lead.company)
        print(res2)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    # report = llm_report(response1.text, response2.text)
    