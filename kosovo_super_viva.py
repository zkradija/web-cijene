import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql


BASE_URL ='https://spv-online-api.tframe.team/customer/products/'

CATEGORIES = [
    ['Kandit','4', '12'],
    ['Kandit', '4', '15'],
    ['Kandit', '4', '14'],
    ['Saponia', '2', '34'],
    ['Saponia', '2', '30'],
    ['Saponia', '2', '36']
]

# url = ?search&category=4&subcategory=12&page=1&sort=description

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()

    for category in CATEGORIES:
        print(category)
        category_name, cat, sub_cat = category
        url_page_number = f'{BASE_URL}?search&category={cat}&subcategory={sub_cat}&page=1&sort=description'
        response = fake_headers(url_page_number, 0)
        data = json.loads(response)
        page_number = int(data['total_pages'])

        for x in range (1,page_number+1):
            url = f'{BASE_URL}?search&category={cat}&subcategory={sub_cat}&page={x}&sort=description'
            r = fake_headers(url, 0)
            data = json.loads(r)

            for product in data['results']:
                code = product['product_id']
                price = float(product['price'])
                if code not in unique_codes and price > 0:
                    products.append([    
                        28, # store
                        str(date.today()),
                        'https://www.super-viva.com/produkt/' + product['product_id'],
                        category_name,
                        code,
                        product['description'],  # name
                        price
                    ])
                    unique_codes.add(code)
                
            time.sleep(1)
    
    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()