import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql


kat =   [['Saponia','https://product-search.services.dmtech.com/hr/search/crawl?allCategories.id=060500&pageSize=10000&sort=editorial_relevance&type=search-static']]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')

    result=[]
    indProxy = 0
    web_site = 17
    store = 27
    date_str = str(date.today())

    start_time = time.time()
    for k in kat:
        print(k)
        r = fake_headers(k[1], indProxy)
        data = json.loads(r)
        for d in data['products']:
            product = []
            product.append(web_site)
            product.append(store)
            product.append(date_str)
            product.append('https://www.dm.hr' + d['relativeProductUrl'])
            product.append(k[0])
            product.append(d['dan'])
            product.append(d['name'])
            product.append(float(float(d['price']['value'])))
            product.append(str(d['gtin'])[:20])
            result.append(product)
        time.sleep(1)
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()