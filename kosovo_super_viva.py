import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql


kat =   [['Kandit','https://spv-online-api.tframe.team/customer/products/',
            '4', '12'],
        ['Kandit', 'https://spv-online-api.tframe.team/customer/products/',
            '4', '15'],
        ['Kandit', 'https://spv-online-api.tframe.team/customer/products/',
            '4', '14'],
        ['Saponia', 'https://spv-online-api.tframe.team/customer/products/',
            '2', '34'],
        ['Saponia', 'https://spv-online-api.tframe.team/customer/products/',
            '2', '30'],
        ['Saponia', 'https://spv-online-api.tframe.team/customer/products/',
            '2', '36']]

# url = ?search&category=4&subcategory=12&page=1&sort=description

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result=[]
    indProxy = 0
    web_site = 18
    trgovina = 28
    date_str = str(date.today())
    start_time = time.time()
    for k in kat:
        print(k)
        url_page_number = f'https://spv-online-api.tframe.team/customer/products/?search&category={k[2]}&subcategory={k[3]}&page=1&sort=description'
        r = fake_headers(url_page_number, indProxy)
        data = json.loads(r)
        page_number = int(data['total_pages'])

        for x in range (1,page_number+1):
            url = f'https://spv-online-api.tframe.team/customer/products/?search&category={k[2]}&subcategory={k[3]}&page={x}&sort=description'
            r = fake_headers(url, indProxy)
            data = json.loads(r)

            for d in data['results']:
                product=[]
                product.append(web_site)
                product.append(trgovina)
                product.append(date_str)
                product.append('https://www.super-viva.com/produkt/' + d['product_id'])
                product.append(k[0])
                product.append(d['product_id'])
                product.append(d['description'])
                product.append(float(d['price']))
                result.append(product)
                
            time.sleep(1)
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()