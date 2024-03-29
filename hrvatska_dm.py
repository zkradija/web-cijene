import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql


CATEGORIES =   [
        ['Saponia','https://product-search.services.dmtech.com/hr/search/crawl?allCategories.id=060500&pageSize=10000&sort=editorial_relevance&type=search-static']
]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()
    
    for category in CATEGORIES:
        print(category)
        category_name, url = category
        response = fake_headers(url, 0)
        data = json.loads(response)
        
        for product in data['products']:
            code = product['dan']
            price = float(product['price']['value'])
            if code not in unique_codes and price > 0:
            # Only add the product if its code is not already in the set
                products.append([
                    27, # store
                    str(date.today()),  # date_str
                    'https://www.dm.hr' + product['relativeProductUrl'],
                    category_name,      # category_name
                    code,
                    product['name'],    # name
                    price
                ])
                unique_codes.add(code)
        
        time.sleep(1)
    
    # Inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()