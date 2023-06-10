import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

kat =   [['Sve','https://www.plodine.hr/akcije/42/tjedna-ponuda/top-brandovi'],
        ['Sve','https://www.plodine.hr/akcije/79/tjedna-ponuda/izdvojeno']]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site = 15
    store = 25
    date_str = str(date.today())
    start_time = time.time()

    for k in kat:
        print(k)
        web_page = fake_headers(k[1], indProxy)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'card__data'}):
            # add product only if it has price
            # some products doesn't have name -> skip them!
            if (div.find('p', {'class': 'regular'}) 
                    and div.find('div',{'class': 'card__heading'}).find('h2')):
                product = []
                product.append(web_site)
                product.append(store)
                product.append(date_str)
                product.append('')  # no link
                product.append(k[0])
                product.append('')
                brand = name = quantity = ''
                if div.find('p',{'class': 'card__description'}):
                    brand = div.find('p',{'class': 'card__description'}).get_text()
                if div.find('h2',{'class': 'card__title'}):
                    title = div.find('h2',{'class': 'card__title'}).get_text()
                if div.find('p',{'class': 'card__quantity'}):
                    quantity = div.find('p',{'class': 'card__quantity'}).get_text()
                    name =f'{brand} {title} {quantity}'
                if name.strip() == '':
                    break
                product.append(name.strip())
                product.append(
                    float(
                        div.find('p', {'class': 'regular'}).get_text()
                        .replace(' €','')
                        .replace(',','.')
                        .strip()
                        )
                )
                result.append(product)
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()