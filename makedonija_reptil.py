import time
from datetime import date, datetime

import cyrtranslit
from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [ 
        ['Kandit', 'https://marketonline.mk/product-category/%D1%85%D1%80%D0%B0%D0%BD%D0%B0/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%B4%D0%B5%D1%81%D0%B5%D1%80%D1%82%D0%B8-%D0%B8-%D0%B3%D1%80%D0%B8%D1%86%D0%BA%D0%B8/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%BA%D0%B0%D0%BA%D0%B0%D0%BE/?per_page=500'],
        ['Kandit', 'https://marketonline.mk/product-category/%D1%85%D1%80%D0%B0%D0%BD%D0%B0/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%B4%D0%B5%D1%81%D0%B5%D1%80%D1%82%D0%B8-%D0%B8-%D0%B3%D1%80%D0%B8%D1%86%D0%BA%D0%B8/%D0%BA%D0%BE%D0%BD%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D1%81%D0%BA%D0%B8-%D0%BF%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D0%B8/%D0%B1%D0%BE%D0%BD%D0%B1%D0%BE%D0%BD%D0%B8-%D1%82%D0%B2%D1%80%D0%B4%D0%B8/?per_page=500'],
        ['Saponia', 'https://marketonline.mk/product-category/%D0%B4%D0%BE%D0%BC%D0%B0%D1%9C%D0%B8%D0%BD%D1%81%D1%82%D0%B2%D0%BE-%D0%B4%D0%BE%D0%BC%D0%B0%D1%9C%D0%B8%D0%BD%D1%81%D1%82%D0%B2%D0%BE/%D0%B4%D0%B5%D1%82%D0%B5%D1%80%D0%B3%D0%B5%D0%BD%D1%82%D0%B8-%D0%BE%D0%BC%D0%B5%D0%BA%D0%BD%D1%83%D0%B2%D0%B0%D1%87%D0%B8/?per_page=500'],
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()
    
    def starts_with_my_class(class_name):
        return class_name and class_name.startswith('product-grid-item product wd-hover-standard')
    
    for category in CATEGORIES:
        print(category)
        category_name, url = category
        
        web_page = fake_headers(url, 0)
        soup = BeautifulSoup(web_page, 'html.parser')
        
        for div in soup.find_all('div', class_=starts_with_my_class):
            code = div.attrs['data-id']
            if code in unique_codes:     # check if code already exists
                pass
            latin_name = cyrtranslit.to_latin(div.find('h3', {'class': 'wd-entities-title'}).get_text(), 'mk')
            product = [
                12,     # website
                22,     # store
                str(date.today()),
                div.find('a')['href'],
                category_name,
                code,           # code
                latin_name,     # name
                float(div.find('span', {'class': 'woocommerce-Price-amount amount'})    # price
                    .get_text()
                    .replace('\xa0ден','')
                    .replace(',', '')
                )
            ]          
            price = product[7]
            if price > 0:
                unique_codes.add(code)
                products.append(product)
            
        time.sleep(1)

    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()