""""
 получение данных из таблицы google drive
 Quick start python and google api - https://developers.google.com/sheets/api/quickstart/python
 install Python client:
   pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

from __future__ import print_function
import pickle
import os.path
from shlex import shlex

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# получение разрешения используя файл json который получается из консоли разработчика
# https://console.developers.google.com/
# создать OAuth 2.0 Client IDs  и выбрать тип Other
def get_credentials_google_api(file_credentials, scopes):
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
                file_credentials, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


# получение доступа Sheets API
def get_sheet_api(creds):
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet


# получение данных с таблицы spreadsheetId в диапазоне range
def get_values_from_spreadsheet(sheet, spreadsheetId, range_cell):
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range=range_cell).execute()
    values = result.get('values', [])
    return values


# ввод данных input_values в range_cell (колонки)
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
def set_values_to_spreadsheet_columns(sheet, spreadsheetid, range_cell, input_values):
    value_input_option = 'RAW'  # ['INPUT_VALUE_OPTION_UNSPECIFIED', 'RAW', 'USER_ENTERED']"
    value_range_body = {
        "majorDimension": "COLUMNS",
        "values": [input_values]
    }
    result = sheet.values().update(spreadsheetId=spreadsheetid, range=range_cell,
                                   valueInputOption=value_input_option, body=value_range_body).execute()
    return result


# ввод данных input_values в range_cell (строки)
# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
def set_values_to_spreadsheet_rows(sheet, spreadsheetid, range_cell, input_values):
    value_input_option = 'RAW'  # ['INPUT_VALUE_OPTION_UNSPECIFIED', 'RAW', 'USER_ENTERED']"
    value_range_body = {
        "majorDimension": "ROWS",
        "values": [input_values]
    }
    result = sheet.values().update(spreadsheetId=spreadsheetid, range=range_cell,
                                   valueInputOption=value_input_option, body=value_range_body).execute()
    return result

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
INPUT_DATA_SPREADSHEET_ID = '12eg1zud0yTR1Lj36V_jju__l8kUTlyWwjvchUnryci4'


def main():
    creds = get_credentials_google_api("credentials2.json", SCOPES)

    sheet = get_sheet_api(creds)

    # получение данных из таблицы и определенного листа
    SAMPLE_RANGE_NAME = 'avito!A1'

    values = get_values_from_spreadsheet(sheet, INPUT_DATA_SPREADSHEET_ID, SAMPLE_RANGE_NAME)

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

    """
    # добавление данных в лист
    SAMPLE_RANGE_NAME2 = 'avito_result!G2:G'
    myvalues = ["15011zasds", "sdsd", "sdsd22", "weq", "eljqwldbqwb"]
    result = set_values_to_spreadsheet_columns(sheet, INPUT_DATA_SPREADSHEET_ID, SAMPLE_RANGE_NAME2, myvalues)
    print(result)

    SAMPLE_RANGE_NAME3 = 'avito_result!C2'
    myvalues2 = ["15011zasds", "sdsd", "sdsd22", "weq", "eljqwldbqwb"]
    result = set_values_to_spreadsheet_rows(sheet, INPUT_DATA_SPREADSHEET_ID, SAMPLE_RANGE_NAME3, myvalues2)
    print(result)
    """


if __name__ == '__main__':
    main()
