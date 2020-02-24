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
        # название товара	цена    цена старая 	адрес	продавец	категория 	описание	ссылка на товар
        row = [tvr.title(), tvr.price(), "", tvr.adress(), tvr.seller(), tvr.category(), tvr.description(),
               tvr.url()]
        mydata.append_values_to_spreadsheet("avito_result!A1", row, False)

    # очистка урлов которые добавил пользователь после обработки
    mydata.clear("avito!A2:A")
    return True


# обработка товаров которые находятся в таблице id_google_table во вкладке sheet
# заголовок таблицы: [название товара, цена, цена старая, адрес, продавец, категория, описание, ссылка на товар]
def check_tovar_price_from_sheet(id_google_table, sheet):
    mydata = GDSheet(id_google_table)
    range = f"{sheet}!A2:H"
    tovar_values = mydata.get_values_from_spreadsheet(range)
    # print(tovar_values[0])
    # создание массива Товаров (Tovar) с ценой которая записана в таблице в столбце "цена"
    array_tovar = []
    for tvr in tovar_values:
        # print(tvr)
        t = Tovar()
        new_tvr = tvr.copy()
        del new_tvr[2]
        # print(new_tvr)
        t.getdata_from_array(new_tvr)
        # print(t)
        array_tovar.append(t)

    array_tovar_newinfo = []
    for i, tvr in enumerate(array_tovar):
        url = tvr.url()
        filename = f"./data/newinfo/{i}.html"
        savefile_from_url(url, filename)

        html_content = ""
        with open(filename, "r", encoding='utf8') as f:
            html_content = f.read()

        avito_tovar = Tovar(url)
        avito_tovar.getdata_from_avito(html_content)
        # print(avito_tovar)
        array_tovar_newinfo.append(avito_tovar)

    for i, tvr in enumerate(array_tovar):
        # TODO: попробовать сделать switch как описано вот тут
        #  https://ru.stackoverflow.com/questions/460207/%D0%95%D1%81%D1%82%D1%8C-%D0%BB%D0%B8-%D0%B2-python-%D0%BE
        #  %D0%BF%D0%B5%D1%80%D0%B0%D1%82%D0%BE%D1%80-switch-case
        tvr_newinfo = array_tovar_newinfo[i]
        if tvr == tvr_newinfo:
            print(f"Цена на товар {i} не изменилась")
        else:
            if tvr < tvr_newinfo:
                print(f"Цена на товар {i} увеличилась")
            else:
                if tvr > tvr_newinfo:
                    print(f"Цена на товар {i} уменьшилась")
        tovar_values[i][2] = tvr.price()
        tovar_values[i][1] = tvr_newinfo.price()

    # изменение цен в гугл таблице
    for i, tvr in enumerate(tovar_values):
        range = f"{sheet}!A{i + 2}:H{i + 2}"
        mydata.set_values_to_spreadsheet(range, tvr, columns=False)

    return True


def main():
    # исходные данные
    id_google_table = '12eg1zud0yTR1Lj36V_jju__l8kUTlyWwjvchUnryci4'
    tovar_sheet = "avito_result"
    # getdata_tovar_from_input_url(id_google_table)

    check_tovar_price_from_sheet(id_google_table, tovar_sheet)


if __name__ == "__main__":
    main()
