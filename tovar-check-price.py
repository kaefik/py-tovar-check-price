"""
  Ссылки на магазин берутся из листа входных данных гугл таблицы, результат работы сохраняется также в гугл таблицу
  в другой лист результата
"""

from tovar import Tovar
from gdsheet import GDSheet
from i_utils import savefile_from_url


# обработка (загрузка информации о товарах) урлов которые добавил пользователь в таблицу
def getdata_tovar_from_input_url(id_google_table):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    mydata = GDSheet(id_google_table)
    input_urls = mydata.get_values_from_spreadsheet("avito!A2:A")
    print(input_urls)
    # END исходные данные

    # получение урлов из результативного листа
    myurldata = mydata.get_values_from_spreadsheet("avito_result!G2:G")
    print(myurldata)
    # END получение урлов из результативного листа

    # оставляем только те урлы которых нет в avito_result
    if len(myurldata) > 0:
        new_input_urls = []

        for input_url in input_urls:
            flag = True
            for myurl in myurldata:
                if myurl[0] == input_url[0]:
                    flag = False
                    break
            if flag:
                new_input_urls.append(input_url)

        if len(new_input_urls) == 0:
            print("Новых ссылок нет. Останавливаем обработку.")
            # очистка урлов которые добавил пользователь после обработки
            mydata.clear("avito!A2:A")
            return False
        input_urls = new_input_urls
    # END оставляем только те урлы которых нет в avito_result

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
        row = [tvr.title(), tvr.price(), tvr.adress(), tvr.seller(), tvr.category(), tvr.description(),
               tvr.url()]
        mydata.append_values_to_spreadsheet("avito_result!A1", row, False)

    # очистка урлов которые добавил пользователь после обработки
    mydata.clear("avito!A2:A")
    return True


def main():
    # исходные данные
    id_google_table = '12eg1zud0yTR1Lj36V_jju__l8kUTlyWwjvchUnryci4'

    getdata_tovar_from_input_url(id_google_table)


if __name__ == "__main__":
    main()
