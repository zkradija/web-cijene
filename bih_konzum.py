import json
import time
from datetime import date, datetime

from headers import headers
from insert_sql import insert_sql

kat = [ ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471252&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723560399'],
        ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471257&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723765060'],
        ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471265&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723789845'],
        ['Saponia', 'https://www.konzumshop.ba/v2/categories/5472087/products?filter%5Bshow%5D=all&filter%5Bsort_field%5D=soldStatistics&filter%5Bsort%5D=soldStatistics&page=1&per_page=1000&time=1685723815904'],
        ['Saponia', 'https://www.konzumshop.ba/v2/categories/5471607/products?filter%5Bshow%5D=all&filter%5Bsort_field%5D=soldStatistics&filter%5Bsort%5D=soldStatistics&page=1&per_page=1000&time=1685723857930'],
        ]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site=11
    store = 21
    date_str = str(date.today())
    start_time = time.time()
    
    for k in kat:
        print[k]
        r = headers(k[1], indProxy)
        data = json.loads(r)

        for d in data['products']:
            product = []
            product.append(web_site)
            product.append(store)
            product.append(date_str)
            product.append('https://www.konzumshop.ba' + d['product_path'])
            product.append(k[0])
            product.append(d['code'])
            product.append(d['name'])
            product.append(float(d['price']['amount'])/100)
            product.append(d['barcodes'][0])
            result.append(product)
            
        time.sleep(1)

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()