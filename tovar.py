from bs4 import BeautifulSoup


# преобразование строки вида "SAMSUNG a50 64\\xd0\\xb3\\xd0\\xb1" в строку c кодировкой encoding
def string_escape(s, encoding="utf-8"):
    import codecs
    byte_s = bytes(s, encoding)
    res = codecs.escape_decode(byte_s)[0]
    res = res.decode(encoding)
    return res


class Tovar(object):

    def __init__(self, url=None):
        # "title"   - заголовок товара
        # "price"   - цена
        # "adress"  - адрес
        # "seller"  - продавец
        # "txt"     - описание
        # "category"- категория
        # "url"     - урл товара
        self.data = dict.fromkeys(["title", "price", "adress", "seller", "txt", "category", "url"])
        self.data["url"] = url

    # получить данные из объявления авито
    def getdata_from_avito(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        # print(soup.prettify())
        # заголовок объявления
        title = soup.select_one('h1[class="title-info-title"]')
        if title is not None:
            title = string_escape(title.text)
            self.data["title"] = title.strip()
        # цена
        price = soup.select_one('span[class="js-item-price"]')
        if price is not None:
            price = price.text.strip()
            price = price.replace(" ", "")
            self.data["price"] = int(price)
        # адрес
        adress = soup.select_one('span[class="item-address__string"]')
        if adress is not None:
            adress = string_escape(adress.text)
            self.data["adress"] = adress.strip()
        # владелец
        seller = soup.select_one('div[class~="seller-info-name"]')
        if seller is not None:
            seller = string_escape(seller.text)
            self.data["seller"] = seller.strip()
        # текст объявления
        txt = soup.select_one('div[class="item-description-text"]')
        if txt is not None:
            txt = string_escape(txt.text)
            self.data["txt"] = txt.strip()

    # сравнение цен товаров ==
    def __eq__(self, other):
        res = self.data["price"] == other.data["price"]
        return res

    # сравнение цен товаров >
    def __gt__(self, other):
        res = self.data["price"] > other.data["price"]
        return res

    # сравнение цен товаров <
    def __lt__(self, other):
        res = self.data["price"] < other.data["price"]
        return res


if __name__ == "__main__":
    filename = "./data/inf.html"
    html_content = ""
    with open(filename, "r", encoding='utf8') as f:
        html_content = f.read()

    avito_tovar = Tovar()
    avito_tovar.getdata_from_avito(html_content)
    print(avito_tovar.data)

    avito_tovar2 = Tovar()
    avito_tovar2.getdata_from_avito(html_content)
    avito_tovar2.data["price"] = 12001
    print(avito_tovar2.data)

    print(avito_tovar < avito_tovar2)
