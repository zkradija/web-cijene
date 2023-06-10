import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql

kat = [ ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-1&substringFilter=pos-visible%3A81701'],
        ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-2&substringFilter=pos-visible%3A81701'],
        ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-3&substringFilter=pos-visible%3A81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-2-1&substringFilter=pos-visible:81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-3&substringFilter=pos-visible:81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-1-1&substringFilter=pos-visible:81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-1-2&substringFilter=pos-visible:81701']]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site=8
    trgovina = 18
    date_str = str(date.today())
    start_time = time.time()
    for k in kat:
        print(k)
        r = fake_headers(k[1], indProxy)
        data = json.loads(r)
        for d in data['hits']:
            product=[]
            product.append(web_site)
            product.append(trgovina)
            product.append(date_str)
            product.append('www.spar.si/online' + d['masterValues']['url'])
            product.append(k[0])
            product.append(d['id'])
            product.append(d['masterValues']['title'] )
            product.append(float(d['masterValues']['best-price']))
            result.append(product)
            
        time.sleep(1)
        
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()