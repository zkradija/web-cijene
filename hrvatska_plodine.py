import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Sve','https://www.plodine.hr/akcije/42/tjedna-ponuda/top-brandovi'],
    ['Sve','https://www.plodine.hr/akcije/79/tjedna-ponuda/izdvojeno']
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    products = []
    start_time = time.perf_counter()

    for category in CATEGORIES:
        print(category)
        category_name, url = category
        web_page = fake_headers(url, 0)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'card__data'}):
            # add product only if it has price
            # some products doesn't have name -> skip them!
            if (div.find('p', {'class': 'regular'}) 
                    and div.find('div',{'class': 'card__heading'}).find('h2')):
                product = [
                    25, # store
                    str(date.today()),
                    '',  # no link
                    category_name,
                    '',     # no code
                ]
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
                product.append(float(div.find('p', {'class': 'regular'}).get_text()
                        .replace(' €','')
                        .replace(',','.')
                        .strip()
                        )
                )
                price = product[7]
                if price > 0:
                    products.append(product)
    
    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()