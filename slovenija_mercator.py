import json
import time
from datetime import date

from headers import headers
from insert_sql import insert_sql

def main():
    result = []
    indProxy = 0
    web_site = 2
    store = 2
    date_str = str(date.today())
    start_time = time.time()

    # Kandit
    for x in range (0,10):
        y = x * 100
        url = f'https://trgovina.mercator.si/market/products/browseProducts/getProducts?limit=100&offset={x}&filterData%5Bcategories%5D=14535711&filterData%5Boffset%5D=8&from={y}&_=1684918912105'
        r = headers(url, indProxy)
        data = json.loads(r)
        for d in data:
            product = []
            if 'data' in d: 
                product.append(web_site)
                product.append(store)
                product.append(date_str)
                product.append('https://trgovina.mercator.si' + d['url']
                               .replace('\\',''))
                product.append('Kandit')
                product.append(d['data']['code'])
                product.append(d['data']['name'])
                product.append(d['data']['current_price'])
                product.append(d['data']['gtins'][0]['gtin'])
                result.append(product)
                print(product)
        time.sleep(1)

    # Saponia
    for x in range (0,7):
        y = x * 100
        url = f'https://trgovina.mercator.si/market/products/browseProducts/getProducts?limit=100&offset={x}&filterData%5Bcategories%5D=14535906&filterData%5Boffset%5D=6&from={y}&_=168493248856'
        r = headers(url,indProxy)
        data = json.loads(r)

        for d in data:
            product = []
            if 'data' in d: 
                product.append(web_site)
                product.append(store)
                product.append(date_str)
                product.append('https://trgovina.mercator.si' + d['url']
                               .replace('\\',''))
                product.append('Saponia')
                product.append(d['data']['code'])
                product.append(d['data']['name'])
                product.append(d['data']['current_price'])
                product.append(d['data']['gtins'][0]['gtin'][:13])
                result.append(product)
                print(product)
        time.sleep(1)

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()