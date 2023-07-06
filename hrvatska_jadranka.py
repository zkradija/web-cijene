import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES =   [
    ['Kandit','https://shop.jadranka-trgovina.com/kategorija-proizvoda/slatkisi-i-grickalice/550-cokolade/'],
    ['Kandit','https://shop.jadranka-trgovina.com/kategorija-proizvoda/slatkisi-i-grickalice/550-bombonjere/'],
    ['Kandit','https://shop.jadranka-trgovina.com/kategorija-proizvoda/slatkisi-i-grickalice/550-bomboni-lizalice-zvakace-gume/'],
    ['Kandit','https://shop.jadranka-trgovina.com/kategorija-proizvoda/slatkisi-i-grickalice/550-snack/'],
    ['Koestlin','https://shop.jadranka-trgovina.com/kategorija-proizvoda/slatkisi-i-grickalice/550-grickalice-krekeri/'],
    ['Koestlin','https://shop.jadranka-trgovina.com/kategorija-proizvoda/slatkisi-i-grickalice/550-keksi-kolaci/'],
    ['Saponia','https://shop.jadranka-trgovina.com/kategorija-proizvoda/kucanstvo-ciscenje-pospremanje/920-pranje-rublja/'],
    ['Saponia','https://shop.jadranka-trgovina.com/kategorija-proizvoda/kucanstvo-ciscenje-pospremanje/920-pranje-posuda'],
    ['Saponia','https://shop.jadranka-trgovina.com/kategorija-proizvoda/kucanstvo-ciscenje-pospremanje/920-sredstva-za-ciscenje-i-ostalo/'],
    ['Saponia','https://shop.jadranka-trgovina.com/kategorija-proizvoda/njega-i-higijena/930-njega-zubi/']
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()

    for category in CATEGORIES:
        for x in range(1,101):   # expecting less then 1000 products / category
            print(f'{category} --> page {x}')
            category_name, url = category
            web_page = fake_headers(f'{url}page/{x}/', 0, None, indVerify=False)
            soup = BeautifulSoup(web_page, 'html.parser')
            
            for div in soup.find_all('div', {'class': 'content'}):
                code = div.find('div', {'class': 'info'}).find('p').get_text().split(':')[1].strip()
                if code in unique_codes:
                    pass
                else:
                    product = [
                        31,
                        str(date.today()),
                        div.find('a')['href'],
                        category_name,
                        code,
                        div.find('p', {'class': 'product-title'}).get_text(),
                        float(
                            div.find('span', {'class': 'product-price'})
                            .get_text()
                            .split('€')[0]
                            .strip()
                        )
                    ]
                    price = product[7]
                    if price > 0:  # Check if price > 0
                        unique_codes.add(product[5])
                        products.append(product)
            if soup.find('a', {'class': 'next page-numbers'}):
                pass
            else:
                break
            time.sleep(2)
                

    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()