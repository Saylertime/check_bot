from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as CREDS
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.calendar import current_month
import os
import gspread


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SAMPLE_SPREADSHEET_ID = "1oJKkYqZ7Ag9D1daix1zR59kYKqQxw1r-hVmM3Qtnegg"

creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())

def get_sheet_names():
    try:
        service = build("sheets", "v4", credentials=creds)

        spreadsheet = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
        sheets = spreadsheet.get('sheets', [])

        sheet_names = [sheet['properties']['title'] for sheet in sheets]
        return sheet_names

    except HttpError as err:
        print(err)
        return None

def get_data_from_sheet(username):
    SAMPLE_RANGE_NAME = "АВТОРЫ!A2:I"

    try:
        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            return None
        for value in values:
            if username in value:
                return value[0]

    except HttpError as err:
        print(err)
        return None


def new_list(username, msg):

    SERVICE_ACCOUNT_FILE = 'noted-aloe-312816-1a7fb3d4ab15.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = CREDS.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(SAMPLE_SPREADSHEET_ID)
    new_sheet_name = str(current_month())

    try:
        spreadsheet.add_worksheet(title=new_sheet_name, rows=100, cols=20)
        print(f'Создан новый лист "{new_sheet_name}')
    except:
        print('Не получилось...')

    try:
        sheet = client.open_by_key(SAMPLE_SPREADSHEET_ID).worksheet(new_sheet_name)
        row = [username, msg]
        sheet.append_row(row)
    except:
        pass











