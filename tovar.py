from bs4 import BeautifulSoup

# преобразование строки вида "SAMSUNG a50 64\\xd0\\xb3\\xd0\\xb1" в строку c кодировкой encoding
def string_escape(s, encoding="utf-8"):
    import codecs
    byte_s = bytes(s, encoding)
    res = codecs.escape_decode(byte_s)[0]
    res = res.decode(encoding)
    return res

class Tovar(object):

    def __init__(self):
        # "title"   - заголовок товара
        # "price"   - цена
        # "adress"  - адрес
        # "seller"  - продавец
        # "txt"     - описание
        # "category"- категория
        # "url"     - урл товара
        self.data = dict.fromkeys(["title", "price", "adress", "seller", "txt", "category", "url"])

    # получить данные из объявления авито
    def getdata_from_avito(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        # print(soup.prettify())
        # заголовок объявления
        title = soup.select_one('h1[class="title-info-title"]').text
        title = string_escape(title)
        self.data["title"] = title.strip()
        # print(tovar)
        # цена
        price = soup.select_one('span[class="js-item-price"]').text
        self.data["price"] = price.strip()
        # print(tovar)
        # адрес
        adress = soup.select_one('span[class="item-address__string"]').text
        adress = string_escape(adress)
        self.data["adress"] = adress.strip()
        # print(tovar)
        # владелец
        seller = soup.select_one('div[class~="seller-info-name"]').text
        seller = string_escape(seller)
        self.data["seller"] = seller.strip()
        # текст объявления
        txt = soup.select_one('div[class="item-description-text"]').text
        txt = string_escape(txt)
        self.data["txt"] = txt.strip()


if __name__ == "__main__":
    filename = "./data/inf.html"
    html_content = ""
    with open(filename, "r", encoding='utf8') as f:
        html_content = f.read()

    avito_tovar = Tovar()
    avito_tovar.getdata_from_avito(html_content)
    print(avito_tovar.data)




