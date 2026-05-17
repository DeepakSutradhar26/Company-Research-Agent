import os
import gspread
import pickle
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES_SHEET = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_ID = '1HXQ8H3T8kSd-7Zz-8fZY2Spcj8tU5-c_enmv0mY7fUI'

def log_to_sheets(lead, pdf_path):
    try:
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES_SHEET)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1

        sheet.append_row([
            lead.name,
            lead.email,
            lead.company,
            lead.url or '',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            pdf_path,
            'generated'
        ])

        return {'success': True}
    except Exception as e:
        return {'success': False, 'message': str(e)}
    
SCOPES_DRIVE = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = '1M1GFEXFeZIEf4-K_ifFuVM-4j-cDE29k'

def _get_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'oauth_credentials.json', SCOPES_DRIVE)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
    return creds

def upload_to_drive(pdf_path: str):
    try:
        creds = _get_creds()
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'name': os.path.basename(pdf_path),
            'parents': [FOLDER_ID]
        }

        media = MediaFileUpload(pdf_path, mimetype='application/pdf')

        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        service.permissions().create(
            fileId=file.get('id'),
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()

        return {
            'success': True,
            'file_id': file.get('id'),
            'url': file.get('webViewLink')
        }
    except Exception as e:
        return {'success': False, 'message': str(e)}