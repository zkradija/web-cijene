import time
from datetime import date, datetime

from bs4 import BeautifulSoup, SoupStrainer

from fake_headers import fake_headers
from insert_sql import insert_sql

kat =   [
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
    result = []
    indProxy = 0
    web_site = 21
    store = 31
    date_str = str(date.today())

    # there is no barcode so im using dummy data
    barcode = ''
    start_time = time.time()
    product_dict = {}

    for k in kat:
        for x in range(1,101):   # expecting less then 1000 products / category
            print(f'{k} --> page {x}')
            web_page = fake_headers(f'{k[1]}page/{x}/', indProxy,'',indVerify=False)
            soup = BeautifulSoup(web_page, 'html.parser')
            for div in soup.find_all('div', {'class': 'content'}):
                code = div.find('div', {'class': 'info'}).find('p').get_text().split(':')[1].strip()  # noqa: E501
                if product_dict.get(code):
                    pass
                else:
                    product = []
                    product.append(web_site)
                    product.append(store)
                    product.append(date_str)
                    product.append(div.find('a')['href'])
                    product.append(k[0])
                    product.append(code)
                    product.append(div.find('p', {'class': 'product-title'}).get_text())
                    product.append(
                        float(
                            div.find('span', {'class': 'product-price'})
                            .get_text()
                            .split('€')[0]
                            .strip()
                        )
                    )
                    product.append(barcode)
                    result.append(product)
                    product_dict[product[5]] = 1
            if soup.find('a', {'class': 'next page-numbers'}):
                pass
            else:
                break
            time.sleep(1)
                

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()