import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql

BASE_URL = 'https://trgovina.mercator.si'

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()
    
    # Kandit
    for x in range (0,10):
        y = x * 100
        url = f'{BASE_URL}/market/products/browseProducts/getProducts?limit=100&offset={x}&filterData%5Bcategories%5D=14535711&filterData%5Boffset%5D=8&from={y}&_=1684918912105'
        print(url)
        response = fake_headers(url, 0)
        data = json.loads(response)
        
        for product in data:
            code = product['data']['code']
            price = float(product['data']['current_price'])
            if code not in unique_codes and price > 0:      # Only add the product if its code is not already in the set
                products.append([
                    2,  # website
                    2,  # store
                    str(date.today()),  # date
                    f'{BASE_URL}{product["url"]}'.replace('\\',''),
                    'Kandit',
                    code,
                    product['data']['name'],
                    price
                    ])
                unique_codes.add(code)
                
        time.sleep(1)

    # Saponia
    for x in range (0,7):
        y = x * 100
        url = f'{BASE_URL}/market/products/browseProducts/getProducts?limit=100&offset={x}&filterData%5Bcategories%5D=14535906&filterData%5Boffset%5D=6&from={y}&_=168493248856'
        print(url)
        response = fake_headers(url,0)
        data = json.loads(response)

        for product in data:
            code = product['data']['code']
            price = float(product['data']['current_price'])
            if code not in unique_codes and price > 0:      # Only add the product if its code is not already in the set
                products.append([
                    2,  # website
                    2,  # store
                    str(date.today()),  # date
                    f'{BASE_URL}{product["url"]}'.replace('\\',''),
                    'Saponia',
                    code,
                    product['data']['name'],
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