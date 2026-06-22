# Company Intelligence Report Generator

Company Intelligence Report Generator is a FastAPI-based AI system that generates structured company intelligence reports from a lead form submission. It collects data from a company website and Wikipedia, processes it using an LLM, and delivers a formatted PDF report via email.

> ## NOTE: Railway free plan doesn't allow Google SMTP (port 587) connections and credentails are not added. So send email, logging to sheets and upload to drive do not work on live link

## Features

- Lead form submission (name, email, company, website)
- Web scraping for company data
- Wikipedia-based company information retrieval
- AI-generated business analysis using Groq LLM (LLaMA 3)
- Structured report generation using Pydantic
- PDF report creation using ReportLab
- Email delivery with PDF attachment
- Google Sheets logging of every lead
- PDF archiving to Google Drive

## Tech Stack

- FastAPI
- LangChain
- Groq LLM
- BeautifulSoup + Requests
- WikipediaRetriever
- ReportLab
- SMTP (Gmail)
- Pydantic
- gspread + Google Sheets API
- Google Drive API

## Flow

1. User submits lead form
2. Website + Wikipedia data is collected
3. LLM generates structured report
4. PDF is created and saved locally
5. PDF is uploaded to Google Drive
6. Report is emailed to user with PDF attached
7. Lead data is logged to Google Sheets

## Google Sheets Live Leads Tracker

Every lead submission is automatically appended to a live Google Sheet including name, email, company, URL, timestamp, PDF path, and report status.

[View Live Leads Sheet](https://docs.google.com/spreadsheets/d/1HXQ8H3T8kSd-7Zz-8fZY2Spcj8tU5-c_enmv0mY7fUI/edit?pli=1&gid=0#gid=0)

## Google Drive PDF Archive

Every generated PDF report is automatically uploaded to a shared Google Drive folder for archival and easy access.

[View Drive Folder](https://drive.google.com/drive/u/0/folders/1M1GFEXFeZIEf4-K_ifFuVM-4j-cDE29k)

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
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Create .env
```
EMAIL=your_email
EMAIL_PASSWORD=your_app_password
GROQ_API_KEY=your_groq_key
```

## Google Services Setup

### Sheets Logging
1. Create a Google Cloud project and enable Google Sheets API
2. Create a service account and download `credentials.json`
3. Share your Google Sheet with the service account email

### Drive Upload
1. Enable Google Drive API in the same project
2. Create an OAuth 2.0 Desktop client and download `oauth_credentials.json`
3. Run `python auth.py` once to generate `token.pickle`
4. Share your Drive folder with the service account or use your personal OAuth token
