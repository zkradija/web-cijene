import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

kat =   [['Sve','https://www.eurospin.hr/akcija/']]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site = 16
    store = 26
    date_str = str(date.today())

    # there is no barcode so im using dummy data
    barcode = ''
    start_time = time.time()

    for k in kat:
        print(k)
        web_page = fake_headers(k[1], indProxy)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'sn_promo_grid_item_ct'}):
            start_date_str = div.find(
                'div', {'class': 'date_current_promo'}).get_text()[0:6]
            end_date_str = div.find(
                'div', {'class': 'date_current_promo'}).get_text()[-6:]
            start_date_str =f'{datetime.now().year}-{start_date_str[3:5]}' \
                            f'-{start_date_str[0:2]}' 
            end_date_str =  f'{datetime.now().year}-{end_date_str[3:5]}' \
                            f'-{end_date_str[0:2]}' 
            
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            if start_date <= datetime.today() <= end_date:
                # add product only if it has price
                if div.find('div', {'class': 'i_price'}).find('i', itemprop='price'):
                    product = []
                    product.append(web_site)
                    product.append(store)
                    product.append(date_str)
                    product.append(div.find('figure')['src']) 
                    product.append(k[0])
                    product.append(div.find('figure')['src']
                                   .split('/')[-1]
                                   .replace('.jpg',''))
                    product.append(div.find('h2').get_text().replace('\n',''))
                    product.append(
                        div.find('div', class_='i_price').find('i', itemprop='price')
                        .get_text()
                        .replace('€ ','')
                        .replace(',','.')
                        .strip()
                    )
                    product.append(barcode)
                    result.append(product)
                else:
                    break
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()