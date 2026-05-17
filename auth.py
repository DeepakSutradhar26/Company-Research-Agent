from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
flow = InstalledAppFlow.from_client_secrets_file('oauth_credentials.json', SCOPES)
creds = flow.run_local_server(port=8080, open_browser=True)

with open('token.pickle', 'wb') as f:
    pickle.dump(creds, f)

print('Done! token.pickle saved.')