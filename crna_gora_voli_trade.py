import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit', 'https://voli.me/kategorije/52'],
    ['Kandit', 'https://voli.me/kategorije/53'],
    ['Kandit', 'https://voli.me/kategorije/54'],
    ['Kandit', 'https://voli.me/kategorije/59'],
    ['Saponia', 'https://voli.me/kategorije/188'],
    ['Saponia', 'https://voli.me/kategorije/189'],
    ['Saponia', 'https://voli.me/kategorije/213'],
    ['Saponia', 'https://voli.me/kategorije/214'],
    ['Saponia', 'https://voli.me/kategorije/216'],
    ['Saponia', 'https://voli.me/kategorije/217'],
    ['Saponia', 'https://voli.me/kategorije/218'],
    ['Saponia', 'https://voli.me/kategorije/220'],
    ['Saponia', 'https://voli.me/kategorije/222'],
    ['Saponia', 'https://voli.me/kategorije/223'],
    ['Saponia', 'https://voli.me/kategorije/224']
 ]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.time()
    products = []
    unique_codes = set()
    
    for category in CATEGORIES:
        print(category)
        category_name, url = category
        web_page = fake_headers(url, 0)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'card-body p-3'}):
            product_href = div.find('div', {'class': 'card-text'}).find('a')['href']
            if product_href.split('/')[-1] in unique_codes:     # check if code already exists
                pass
            product = [
                10,     # website
                20,     # store
                str(date.today()),  # date
                str(product_href),  # product url
                category_name,  
                product_href.split('/')[-1],    # code
                div.find('div', {'class': 'card-text'}).get('title').strip()    # name
            ]

            if div.find('div',{'class':'product-price pl-special text-primary'}):
                product.append(float(div.find('div',{'class': 'price-wrapper'})
                        .find('div',{'class': 'product-price pl-special text-primary'})
                        .get_text().strip().split('€')[0].replace(',','')))
            else: 
                product.append(float(div.find('div',{'class': 'price-wrapper'})
                        .find('div',{'class': 'product-price text-secondary'})
                        .get_text().strip().split('€')[0].replace(',','')))
            
            price = product[7]
            if price > 0:  # Check if price > 0
                unique_codes.add(product[5])
                products.append(product)
            
        time.sleep(1)

    
    # inserting data
    insert_sql(products)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()