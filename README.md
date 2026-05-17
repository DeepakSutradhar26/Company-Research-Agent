# SimplifIQ – AI Company Intelligence Report Generator

SimplifIQ is a FastAPI-based AI system that generates structured company intelligence reports from a lead form submission. It collects data from a company website and Wikipedia, processes it using an LLM, and delivers a formatted PDF report via email.

## Features

- Lead form submission (name, email, company, website)
- Web scraping for company data
- Wikipedia-based company information retrieval
- AI-generated business analysis using Groq LLM (LLaMA 3)
- Structured report generation using Pydantic
- PDF report creation using ReportLab
- Email delivery with PDF attachment
- Optional Google Sheets logging

## Tech Stack

- FastAPI  
- LangChain  
- Groq LLM  
- BeautifulSoup + Requests  
- WikipediaRetriever  
- ReportLab  
- SMTP (Gmail)  
- Pydantic  

## Flow

1. User submits lead form  
2. Website + Wikipedia data is collected  
3. LLM generates structured report  
4. PDF is created  
5. Report is emailed to user  

## API

### POST /submit-lead

Request:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "OpenAI",
  "url": "https://openai.com"
}
```

Response:
```json
{
  "success": true,
  "message": "Email sent to john@example.com"
}
```

## Setup
```
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Create .env:
```
EMAIL=your_email
EMAIL_PASSWORD=your_password
GROQ_API_KEY=your_key
```