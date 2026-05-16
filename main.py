from requests import Request
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from schema.form_submission import LeadInput

app = FastAPI()

template = Jinja2Templates(directory='templates')

@app.get('/')
def home(request: Request):
    return template.TemplateResponse('index.html',{'request':request})

@app.post('/submit-lead')
def submit_lead(lead : LeadInput):
    pass

