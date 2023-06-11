import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-1&substringFilter=pos-visible%3A81701'],
    ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-2&substringFilter=pos-visible%3A81701'],
    ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-3&substringFilter=pos-visible%3A81701'],
    ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-2-1&substringFilter=pos-visible:81701'],
    ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-3&substringFilter=pos-visible:81701'],
    ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-1-1&substringFilter=pos-visible:81701'],
    ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-1-2&substringFilter=pos-visible:81701']
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()  # Set to store unique product codes
    
    for category in CATEGORIES:
        print(category)
        category_name, url = category
        r = fake_headers(url, 0)
        data = json.loads(r)
        for product in data['hits']:
            code = product['id']
            price = float(product['masterValues']['best-price'])
            products.append([
                8,      # website
                18,     # store
                str(date.today()),
                f'www.spar.si/online{product["masterValues"]["url"]}',
                category_name,
                code,
                product['masterValues']['title'],   # name
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