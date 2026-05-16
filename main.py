from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from schema.form_submission import LeadInput
from services.web_scraper import scrape_company_data

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
    data = scrape_company_data(lead.url)
    print(data)