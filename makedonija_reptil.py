import time
from datetime import date

import cyrtranslit
from bs4 import BeautifulSoup

from headers import headers
from insert_sql import insert_sql

kat =   [ 
        ['Kandit', 'https://marketonline.mk/product-category/%D1%85%D1%80%D0%B0%D0%BD%D0%B0/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%B4%D0%B5%D1%81%D0%B5%D1%80%D1%82%D0%B8-%D0%B8-%D0%B3%D1%80%D0%B8%D1%86%D0%BA%D0%B8/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%BA%D0%B0%D0%BA%D0%B0%D0%BE/?per_page=500'],
        ['Kandit', 'https://marketonline.mk/product-category/%D1%85%D1%80%D0%B0%D0%BD%D0%B0/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%B4%D0%B5%D1%81%D0%B5%D1%80%D1%82%D0%B8-%D0%B8-%D0%B3%D1%80%D0%B8%D1%86%D0%BA%D0%B8/%D0%BA%D0%BE%D0%BD%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D1%81%D0%BA%D0%B8-%D0%BF%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D0%B8/%D0%B1%D0%BE%D0%BD%D0%B1%D0%BE%D0%BD%D0%B8-%D1%82%D0%B2%D1%80%D0%B4%D0%B8/?per_page=500'],
        ['Saponia', 'https://marketonline.mk/product-category/%D0%B4%D0%BE%D0%BC%D0%B0%D1%9C%D0%B8%D0%BD%D1%81%D1%82%D0%B2%D0%BE-%D0%B4%D0%BE%D0%BC%D0%B0%D1%9C%D0%B8%D0%BD%D1%81%D1%82%D0%B2%D0%BE/%D0%B4%D0%B5%D1%82%D0%B5%D1%80%D0%B3%D0%B5%D0%BD%D1%82%D0%B8-%D0%BE%D0%BC%D0%B5%D0%BA%D0%BD%D1%83%D0%B2%D0%B0%D1%87%D0%B8/?per_page=500'],
        ]

def main():
    result = []
    indProxy = 0
    web_site=12
    store = 22
    date_str = str(date.today())

    # there is no gtin_kom so im using dummy data
    gtin_kom = ''    
    start_time = time.time()

    def starts_with_my_class(class_name):
        return class_name and class_name.startswith(
            'product-grid-item product wd-hover-standard'
            )
    
    for k in kat:
        web_page = headers(k[1], indProxy)
        soup = BeautifulSoup(web_page, 'html.parser')
        for div in soup.find_all('div', class_=starts_with_my_class):
            product = []
            product.append(web_site)
            product.append(store)
            product.append(date_str)
            product.append(div.find('a')['href'])
            product.append(k[0])
            product.append(div.attrs['data-id'])
            latin_name = cyrtranslit.to_latin(
                div.find('h3', {'class': 'wd-entities-title'}).get_text(), 'mk'
                )
            product.append(latin_name)
            product.append(
                float(
                    div.find('span', {'class': 'woocommerce-Price-amount amount'})
                    .get_text()
                    .replace('\xa0ден','')
                    .replace(',', '')
                )
            )
            product.append(gtin_kom)
            result.append(product)
            print(product)
        time.sleep(1)

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()