""""
 Работа с классом Таблиц Google Docs
 Quick start python and google api - https://developers.google.com/sheets/api/quickstart/python
 install Python client (library):
   pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
"""

import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# ------ Вспомогательные функции --------------
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


# ------ END Вспомогательные функции --------------

# класс для работы с Таблицей Google Docs
class GDSheet:

    def __init__(self, spreadsheetId, file_credentials="credentials.json",
                 scopes=['https://www.googleapis.com/auth/spreadsheets']):
        self.spreadsheetId = spreadsheetId  # индекс гугл таблицы
        self.creds = get_credentials_google_api(file_credentials, scopes)
        self.sheet = get_sheet_api(self.creds)

    # получение данных с таблицы spreadsheetId в диапазоне range
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
    def get_values_from_spreadsheet(self, range_cell):
        result = self.sheet.values().get(spreadsheetId=self.spreadsheetId,
                                         range=range_cell).execute()
        values = result.get('values', [])
        return values

    # ввод данных input_values в range_cell
    # columns=True - изменение в колонках, иначе изменение в строках
    # value_input_option может принимать следующие значения: ["INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED"]
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
    def set_values_to_spreadsheet(self, range_cell, input_values, columns=True,
                                  value_input_option="RAW"):
        majorDimension = "COLUMNS" if columns else "ROWS"
        value_range_body = {
            "majorDimension": majorDimension,
            "values": [input_values]
        }
        result = self.sheet.values().update(spreadsheetId=self.spreadsheetId, range=range_cell,
                                            valueInputOption=value_input_option, body=value_range_body).execute()
        return result

    # ввод данных input_values в range_cell
    # columns=True - изменение в колонках, иначе изменение в строках
    # value_input_option может принимать следующие значения: ["INPUT_VALUE_OPTION_UNSPECIFIED", "RAW", "USER_ENTERED"]
    # insert_data_option может принимать следующие значения: OVERWRITE или INSERT_ROWS
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
    def append_values_to_spreadsheet(self, range_cell, input_values, columns=True,
                                     value_input_option="RAW", insert_data_option="OVERWRITE"):
        majorDimension = "COLUMNS" if columns else "ROWS"
        value_range_body = {
            "majorDimension": majorDimension,
            "values": [input_values]
        }

        result = self.sheet.values().append(spreadsheetId=self.spreadsheetId, range=range_cell,
                                            valueInputOption=value_input_option, insertDataOption=insert_data_option,
                                            body=value_range_body).execute()
        return result

    # очиска ячеек указанных в ranfe_cell
    def clear(self, range_cell):
        result = self.sheet.values().clear(spreadsheetId=self.spreadsheetId, range=range_cell).execute()
        return result


__all__ = ("GDSheet")

def main():
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    INPUT_DATA_SPREADSHEET_ID = '12eg1zud0yTR1Lj36V_jju__l8kUTlyWwjvchUnryci4'

    mydata = GDSheet(INPUT_DATA_SPREADSHEET_ID)

    # получение данных из таблицы и определенного листа
    SAMPLE_RANGE_NAME = 'avito!A1:A'
    values = mydata.get_values_from_spreadsheet(SAMPLE_RANGE_NAME)
    print(values)

    # mydata.clear('avito_result!G:G')

    # добавление данных в лист
    SAMPLE_RANGE_NAME2 = 'avito_result!A1'
    myvalues = ["15011zasds", "sdsd", "sdsd22", "weq", "eljqwldbqwb"]
    mydata.append_values_to_spreadsheet(SAMPLE_RANGE_NAME2, myvalues)

    """
    # добавление данных в лист
    SAMPLE_RANGE_NAME2 = 'avito_result!G2:G'
    myvalues = ["15011zasds", "sdsd", "sdsd22", "weq", "eljqwldbqwb"]
    result = mydata.set_values_to_spreadsheet(SAMPLE_RANGE_NAME2, myvalues)
    print(result)

    SAMPLE_RANGE_NAME3 = 'avito_result!C2'
    myvalues2 = ["hello", "poka", "xoxoxox", "weq", "eljqwldbqwb"]
    result = mydata.set_values_to_spreadsheet(SAMPLE_RANGE_NAME3, myvalues2, False)
    print(result)
    """


if __name__ == '__main__':
    main()
