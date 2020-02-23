"""
  Ссылки на магазин берутся из листа входных данных гугл таблицы, результат работы сохраняется также в гугл таблицу
  в другой лист результата
"""

from tovar import Tovar
from gdsheet import GDSheet
from i_utils import savefile_from_url


def main():
    # исходные данные
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    id_google_table = '12eg1zud0yTR1Lj36V_jju__l8kUTlyWwjvchUnryci4'

    mydata = GDSheet(id_google_table)
    SAMPLE_RANGE_NAME = 'avito!A2:A'
    input_urls = mydata.get_values_from_spreadsheet(SAMPLE_RANGE_NAME)
    print(input_urls)
    # END исходные данные

    avito_tovars = []
    for i, url_item in enumerate(input_urls):
        url = url_item[0]
        filename = f"./data/{i}.html"
        savefile_from_url(url, filename)

        html_content = ""
        with open(filename, "r", encoding='utf8') as f:
            html_content = f.read()

        avito_tovar = Tovar(url)
        avito_tovar.getdata_from_avito(html_content)

        avito_tovars.append(avito_tovar)

    for tvr in avito_tovars:
        print(tvr)
        # название товара	цена	адрес	продавец	категория 	описание	ссылка на товар
        row = [tvr.title(), tvr.price(), tvr.adress(), tvr.seller(), tvr.description(), tvr.category(),
               tvr.url()]
        mydata.append_values_to_spreadsheet("avito_result!A1", row, False)


if __name__ == "__main__":
    main()
