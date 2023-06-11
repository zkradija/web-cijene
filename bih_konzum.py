import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql


CATEGORIES = [
    ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471252&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723560399'],
    ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471257&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723765060'],
    ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471265&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723789845'],
    ['Saponia', 'https://www.konzumshop.ba/v2/categories/5472087/products?filter%5Bshow%5D=all&filter%5Bsort_field%5D=soldStatistics&filter%5Bsort%5D=soldStatistics&page=1&per_page=1000&time=1685723815904'],
    ['Saponia', 'https://www.konzumshop.ba/v2/categories/5471607/products?filter%5Bshow%5D=all&filter%5Bsort_field%5D=soldStatistics&filter%5Bsort%5D=soldStatistics&page=1&per_page=1000&time=1685723857930'],
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()  # Set to store unique product codes
    
    for category in CATEGORIES:
        print(category)
        category_name, url = category
        response = fake_headers(url, 0)
        data = json.loads(response)

        for product in data['products']:
            code = product['code']
            price = float(product['price']['amount']) / 100
            if code not in unique_codes and price > 0:      # Only add the product if its code is not already in the set
                products.append([
                    11,  # website
                    21,  # store
                    str(date.today()),
                    'https://www.konzumshop.ba' + product['product_path'],
                    category_name,
                    code,  # code
                    product['name'],  # name
                    price  # price
                ])
                unique_codes.add(code)
            
        time.sleep(1)

    # Inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()