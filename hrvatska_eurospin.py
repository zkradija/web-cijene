import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Sve','https://www.eurospin.hr/akcija/']
    ]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()  # Set to store unique codes
    
    for category in CATEGORIES:
        print(category)
        category_name, url = category        
        web_page = fake_headers(url, 0)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'sn_promo_grid_item_ct'}):
            start_date_str = div.find(
                'div', {'class': 'date_current_promo'}).get_text()[0:6]
            end_date_str = div.find(
                'div', {'class': 'date_current_promo'}).get_text()[-6:]
            start_date_str =f'{datetime.now().year}-{start_date_str[3:5]}' \
                            f'-{start_date_str[0:2]}' 
            end_date_str =  f'{datetime.now().year}-{end_date_str[3:5]}' \
                            f'-{end_date_str[0:2]}' 
            
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            if start_date <= datetime.today() <= end_date:
                # add product only if price exists
                if div.find('div', {'class': 'i_price'}).find('i', itemprop='price'):
                    code = div.find('figure')['src'].split('/')[-1].replace('.jpg','')
                    if code not in unique_codes:     # check if code already exists
                        product = [
                            16,     # web_site
                            26,     # store
                            str(date.today()),  # date_str
                            div.find('figure')['src'],
                            category_name
                        ]
                        product.append(code)
                        product.append(div.find('h2').get_text().replace('\n',''))
                        product.append(
                            float(div.find('div', class_='i_price')
                                .find('i', itemprop='price')
                                .get_text()
                                .replace('€ ','')
                                .replace(',','.')
                                .strip())
                        )
                    price = product[7]
                    if price > 0:  # Check if price > 0
                        unique_codes.add(product[5])
                        products.append(product)
                else:
                    break
    
    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()