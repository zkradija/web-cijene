import time
from datetime import date, datetime
import re

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES =   [
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
    start_time = time.perf_counter()
    products = []
    unique_codes = set()  # Set to store unique product codes

    for category in CATEGORIES:
        print(category)
        category_name, url = category
        web_page = fake_headers(f'{url}', 0)
        soup = BeautifulSoup(web_page, 'html.parser')
        
        for div in soup.find_all('div', {'class': 'article-item'}):
            code = div.find('a', {'class': 'article-add-to-fav'}).attrs['onclick'].split(',')[1].strip()
            if code in unique_codes:
                pass
            else:
                product = [
                    32, # store
                    str(date.today()),
                    f'https://www.ppkbjelovar.com{div.find("h2").find("a")["href"]}',
                    category_name,
                    code,
                    div.find('h2').find('a').get_text(),    # name
                ]
                prices_str = re.findall(
                    r'\d+,\d+', div.find('p', {'class': 'euro-price'}).get_text())
                prices_float = [float(price.replace(',', '.'))  
                                for price in prices_str 
                                if float(price.replace(',', '.')) > 0]
                min_price = min(prices_float)
                if min_price > 0:
                    product.append(min_price)
                    products.append(product)
                    unique_codes.add(code)
        time.sleep(1)
                

    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()