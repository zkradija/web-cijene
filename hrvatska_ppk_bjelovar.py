import time
from datetime import date, datetime
import re

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

kat =   [
        ['Kandit','https://www.ppkbjelovar.com/cokolade-i-kakao-ploce.aspx?size=all'],
        ['Kandit','https://www.ppkbjelovar.com/bomboni-lizalice-zvakace-gume.aspx?size=all'],
        ['Kandit','https://www.ppkbjelovar.com/bombonijere.aspx?size=all'],
        ['Koestlin','https://www.ppkbjelovar.com/grickalice.aspx?size=all'],
        ['Koestlin','https://www.ppkbjelovar.com/keksi-i-vafel-proizvodi.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/tekuci-deterdzenti.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/praskasti-deterdzenti.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/kapsule-i-diskovi.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/omeksivaci.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/tekuci-deterdzenti-v2.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/ostalo.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/sredstva-za-ciscenje.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/wc-osvjezivaci.aspx?size=all'],
        ['Saponia','https://www.ppkbjelovar.com/zubne-paste.aspx?size=all']
        ]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site = 22
    store = 32
    date_str = str(date.today())

    # there is no barcode so im using dummy data
    barcode = ''
    start_time = time.time()
    product_dict = {}

    for k in kat:
        print(k)
        web_page = fake_headers(f'{k[1]}', indProxy,'')
        soup = BeautifulSoup(web_page, 'html.parser')
        for div in soup.find_all('div', {'class': 'article-item'}):
            code = div.find('a', {'class': 'article-add-to-fav'}).attrs['onclick'].split(',')[1].strip()  # noqa: E501
            if product_dict.get(code):
                pass
            else:
                product = []
                product.append(web_site)
                product.append(store)
                product.append(date_str)
                product.append(f'https://www.ppkbjelovar.com{div.find("h2").find("a")["href"]}')
                product.append(k[0])
                product.append(code)
                product.append(div.find('h2').find('a').get_text())
                prices_str = re.findall(
                    r'\d+,\d+', div.find('p', {'class': 'euro-price'}).get_text())
                prices_float = [float(price.replace(',', '.')) 
                               for price in prices_str 
                               if float(price.replace(',', '.')) > 0]
                min_price = min(prices_float)
                product.append(min_price)
                product.append(barcode)
                result.append(product)
                product_dict[product[5]] = 1
        time.sleep(1)
                

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()