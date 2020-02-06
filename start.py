import requests
from bs4 import BeautifulSoup


# from requests_ntlm import HttpNtlmAuth  # https://github.com/requests/requests-ntlm
# используется библиотека - https://github.com/jborean93/ntlm-auth

# преобразование строки вида "SAMSUNG a50 64\\xd0\\xb3\\xd0\\xb1" в строку c кодировкой encoding
def string_escape(s, encoding="utf-8"):
    import codecs
    byte_s = bytes(s, encoding)
    res = codecs.escape_decode(byte_s)[0]
    res = res.decode(encoding)
    return res


# сохранить в файл html из urls
def savefile_from_url(urls, filename):
    session = requests.Session()
    # session.auth = HttpNtlmAuth(user_auth, passw_auth)
    r = session.get(urls)
    print(r.status_code)

    if (r.status_code == 200):
        # print(r.headers)
        print(r.content)

        html = str(r.content)

        with open(filename, "w") as f:
            f.write(html)
        return True
    return False


# получить данные из объявления авито
def getdata_from_avito(html_content):
    tovar = dict.fromkeys(["title", "price", "adress", "seller"])
    soup = BeautifulSoup(html_content, "html.parser")
    # print(soup.prettify())
    # заголовок объявления
    title = soup.select_one('h1[class="title-info-title"]').text
    title = string_escape(title)
    tovar["title"] = title.strip()
    # print(tovar)
    # цена
    price = soup.select_one('span[class="js-item-price"]').text
    tovar["price"] = price.strip()
    # print(tovar)
    # адрес
    adress = soup.select_one('span[class="item-address__string"]').text
    adress = string_escape(adress)
    tovar["adress"] = adress.strip()
    # print(tovar)
    # владелец
    seller = soup.select_one('div[class~="seller-info-name"]').text
    seller = string_escape(seller)
    tovar["seller"] = seller.strip()
    print(tovar)


if __name__ == "__main__":
    """
    # активное объявление
    url = "https://www.avito.ru/kazan/telefony/samsung_a50_64gb_1855500408"
    filename = "data/inf.html"
    # END активное объявление

    # объявление снято с публикации
    url = "https://www.avito.ru/kazan/audio_i_video/kolonki_microlab_m-520_1877143706"
    filename = "data/inf_snyato.html"
    # END объявление снято с публикации

    savefile_from_url(url, filename)
    """

    filename = "data/inf.html"
    html_content = ""
    with open(filename, "r", encoding='utf8') as f:
        html_content = f.read()

    getdata_from_avito(html_content)
