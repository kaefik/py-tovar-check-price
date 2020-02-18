""""
 получение данных из таблицы google drive

 Quick start python and google api - https://developers.google.com/sheets/api/quickstart/python
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.update']

# The ID and range of a sample spreadsheet.
INPUT_DATA_SPREADSHEET_ID = '12eg1zud0yTR1Lj36V_jju__l8kUTlyWwjvchUnryci4'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    SAMPLE_RANGE_NAME = 'avito!A:A'
    result = sheet.values().get(spreadsheetId=INPUT_DATA_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print(values)
        print(len(values))
        """
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
        """

    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
    # https://github.com/googleapis/google-api-python-client
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
    SAMPLE_RANGE_NAME2 = 'avito_result!G:G'
    result = sheet.values().update(spreadsheetId=INPUT_DATA_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME2).execute()

if __name__ == '__main__':
    main()