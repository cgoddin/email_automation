from __future__ import print_function

import base64
import json
import os
import pickle
from datetime import datetime as dt
from datetime import timedelta as td
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import gspread
import pandas as pd
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from gspread_dataframe import set_with_dataframe


def config(config_file):
    path = Path(config_file)
    with open(path,'r') as f:
        config = json.load(f)
    return config

def get_credentials():
    credentials = None

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists(TOKEN):
        print('Loading Credentials From File...')
        with open(TOKEN, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET,
                scopes=['https://www.googleapis.com/auth/gmail.compose','https://www.googleapis.com/auth/documents.readonly','https://www.googleapis.com/auth/spreadsheets']
            )

            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open(TOKEN, 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)
    return credentials

def open_doc(doc_id,credentials):
    docs_service = build('docs', 'v1', discoveryServiceUrl=DISCOVERY_DOC, credentials=credentials)
    # Gives service account access to doc
    doc = docs_service.documents().get(documentId=doc_id).execute()
    doc_content = doc.get('body').get('content')
    return doc_content

def read_doc(content):
    # Reads document text
    components = []
    component = ''
    for element in content:
        if 'paragraph' in element:
            paragraph = element.get('paragraph').get('elements')
            for element in paragraph:
                component += element.get('textRun').get('content')
        elif 'table' in element:
            table = element.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    components.append(read_doc(cell.get('content'))[0])
    components.append(component)
    return components

def get_var(prospect,credentials):
    
    # Compiling callable variables based on pipeline location
    stage = int(prospect['Stage'])
 
    if stage == 0:
        doc_content = open_doc(DOC_IDS['Email 1'],credentials)
        send_time = 'Send Time 1'
        send_id = 'Send ID 1'

    elif stage == 1:
        doc_content = open_doc(DOC_IDS['Email 2'],credentials)
        send_time = 'Send Time 2'
        send_id = 'Send ID 2'
    elif stage == 2:
        doc_content = open_doc(DOC_IDS['Email 3'],credentials)
        send_time = 'Send Time 3'
        send_id = 'Send ID 3'
    elif stage == 3:
        doc_content = open_doc(DOC_IDS['Email 4'],credentials)
        send_time = 'Send Time 4'
        send_id = 'Send ID 4'
    elif stage == 4:
        doc_content = open_doc(DOC_IDS['Email 5'],credentials) 
        send_time = 'Send Time 5'
        send_id = 'Send ID 5'

    subject = read_doc(doc_content)[0]
    body = read_doc(doc_content)[1]

    subject = subject.format(contact=prospect['Contact'])
    body = body.format(contact=prospect['Contact'],business=prospect['Business'],personalization=prospect['Personalization'])

    return subject,body,send_time,send_id

def create_draft(prospect,credentials):

    subject = get_var(prospect,credentials)[0]
    body = get_var(prospect,credentials)[1]

    message = MIMEMultipart()
    message['from'] = FROM_ADR
    message['to'] = prospect['Email']
    message['subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    raw_string = base64.urlsafe_b64encode(message.as_bytes()).decode()

    gmail_service = build('gmail', 'v1', credentials=credentials)

    try:
        draft = gmail_service.users().drafts().create(
            userId='me', 
            body= {'message': {'raw':raw_string }}
        ).execute()

        return draft['id']
    
    except:
        return 'Error creating draft'

def weekday(datetime):    
    weekend = [5,6]
    while datetime.weekday() in weekend:
        datetime += td(days=1)
    return datetime

def send_mail(prospect,credentials):
    gmail_service = build('gmail', 'v1', credentials=credentials)
    try:
        draft = gmail_service.users().drafts().get(
            userId='me',
            id=prospect['Draft ID']).execute()
        send = gmail_service.users().drafts().send(
            userId='me', 
            body= draft
        ).execute()

        return send['id']

    except:
        return 'Error sending draft'

CONFIG = config('.config/config.json') 
FROM_ADR = CONFIG['FromAddress']
CLIENT_SECRET = CONFIG['ClientSecretFile']
TOKEN = CONFIG['Token']
DISCOVERY_DOC = CONFIG['DiscoveryDoc']
SHEET_ID = CONFIG['SheetID']
DOC_IDS = {
'Email 1': CONFIG['DocumentIDs'][0],
'Email 2': CONFIG['DocumentIDs'][1],
'Email 3': CONFIG['DocumentIDs'][2],
'Email 4': CONFIG['DocumentIDs'][3],
'Email 5': CONFIG['DocumentIDs'][4],
}
TIME_DELTAS = {
'td1': CONFIG['TimeDeltas'][0],
'td2': CONFIG['TimeDeltas'][1],
'td3': CONFIG['TimeDeltas'][2],
'td4': CONFIG['TimeDeltas'][3],
}

def main():
    
    # Creates Google API Services w/ credentials
    credentials = get_credentials()

    # Gets data from google sheets
    client = gspread.Client(credentials)
    sheet = client.open_by_key(SHEET_ID).get_worksheet(0)
    prospects = pd.DataFrame(sheet.get_all_records())
    dtype = {
        'Send Time 1': 'datetime64',
        'Send Time 2': 'datetime64',
        'Send Time 3': 'datetime64',
        'Send Time 4': 'datetime64',
        'Send Time 5': 'datetime64',
    }
    prospects = prospects.astype(dtype)

    now = dt.now().replace(second=0,microsecond=0)

    for i in prospects.index:
        
        if prospects.loc[i,'Stage'] == '':
                prospects.loc[i,'Stage'] = 0
                prospects.loc[i,'Send Time 1'] = weekday(now)
                prospects.loc[i,'Send Time 2'] = weekday(prospects.loc[i,'Send Time 1'] + td(days=TIME_DELTAS['td1']))
                prospects.loc[i,'Send Time 3'] = weekday(prospects.loc[i,'Send Time 2'] + td(days=TIME_DELTAS['td2']))
                prospects.loc[i,'Send Time 4'] = weekday(prospects.loc[i,'Send Time 3'] + td(days=TIME_DELTAS['td3']))
                prospects.loc[i,'Send Time 5'] = weekday(prospects.loc[i,'Send Time 4'] + td(days=TIME_DELTAS['td4']))
                
                prospects.loc[i,'Draft ID'] = create_draft(prospects.loc[i],credentials)
        
        if not prospects.loc[i,'Stage'] == 5:
            send_time = get_var(prospects.loc[i],credentials)[2]
            send_id = get_var(prospects.loc[i],credentials)[3]
            
            if prospects.loc[i,send_time] <= now:
                    prospects.loc[i,send_id] = send_mail(prospects.loc[i],credentials)
                    prospects.loc[i,'Stage'] += 1
                    if not prospects.loc[i,'Stage'] == 5:
                        prospects.loc[i,'Draft ID'] = create_draft(prospects.loc[i],credentials)
                    else:
                        prospects.loc[i,'Draft ID'] = '--------------------'
                        prospects.loc[i,'End Date'] = now.date()
                        prospects.loc[i,'End Reason'] = 'Complete'             
    
    set_with_dataframe(sheet, prospects)

def gcp_func_entry(request):
    
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    
    main()
    
    return "Processing Completed!"
