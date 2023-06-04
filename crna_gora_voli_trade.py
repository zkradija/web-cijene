import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from headers import headers
from insert_sql import insert_sql

kat =   [['Kandit','https://voli.me/kategorije/52'],
        ['Kandit','https://voli.me/kategorije/53'],
        ['Kandit','https://voli.me/kategorije/54'],
        ['Kandit','https://voli.me/kategorije/59'],
        ['Saponia','https://voli.me/kategorije/188'],
        ['Saponia','https://voli.me/kategorije/189'],
        ['Saponia','https://voli.me/kategorije/213'],
        ['Saponia','https://voli.me/kategorije/214'],
        ['Saponia','https://voli.me/kategorije/216'],
        ['Saponia','https://voli.me/kategorije/217'],
        ['Saponia','https://voli.me/kategorije/218'],
        ['Saponia','https://voli.me/kategorije/220'],
        ['Saponia','https://voli.me/kategorije/222'],
        ['Saponia','https://voli.me/kategorije/223'],
        ['Saponia','https://voli.me/kategorije/224']]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site = 10
    trgovina = 20
    date_str = str(date.today())
    barcode = ''
    start_time = time.time()
    product_dict = {}
    for k in kat:
        print(k)
        web_page = headers(k[1], indProxy)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'card-body p-3'}):
            if str(div.find('div', {'class': 'card-text'})
                   .find('a')['href']).split('/')[-1] in product_dict:
                break
            product = []
            product.append(web_site)
            product.append(trgovina)
            product.append(date_str)
            product.append(str(div.find('div', {'class': 'card-text'})
                               .find('a')['href']))
            product.append(k[0])
            product.append(str(div.find('div', {'class': 'card-text'})
                .find('a')['href']).split('/')[-1])
            product.append(div.find('div', {'class': 'card-text'}).get('title').strip())
            if div.find('div',{'class':'product-price pl-special text-primary'}):
                product.append(float(div.find('div',{'class': 'price-wrapper'})
                    .find('div',{'class': 'product-price pl-special text-primary'})
                    .get_text().strip().split('€')[0].replace(',','')))
            else: 
                product.append(float(div.find('div',{'class': 'price-wrapper'})
                    .find('div',{'class': 'product-price text-secondary'})
                    .get_text().strip().split('€')[0].replace(',','')))
            product_dict[product[5]]=1
            product.append(barcode)
            result.append(product)
            
        time.sleep(1)

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()