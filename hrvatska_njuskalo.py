import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

store_dict = {
    'Boso': 10,
    'Interspar': 11,
    'Kaufland': 12,
    'Lidl': 13,
    'NTL': 14,
    'Plodine': 15,
    'SPAR': 16,
    'Studenac': 17}

store_list = list(store_dict.keys())

kat =   [['Kandit','slatkisi-grickalice'],
        ['Saponia','paste-za-zube'],
        ['Saponia','deterdzenti-za-rublje'],
        ['Saponia','omeksivaci-za-rublje'],
        ['Saponia','deterdzenti-za-posude'],
        ['Saponia','sredstva-za-ciscenje']]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0    # not using Proxies cuz of 2 much links
    web_site = 7
    date_str = str(date.today())
    start_time = time.time()

    for t in store_list:
        for k in kat:
            print(k)
            # 10 pages / store is more than enough
            for x in range(1,11):   
                url=f'https://popusti.njuskalo.hr/trgovina/{t}/{k[1]}?page={x}&ajax=1&xitiIndex=16'
                web_page = fake_headers(url, indProxy)
                soup = BeautifulSoup(web_page, 'html.parser')
                # don't know exact page numbers, so i'm checking if element exist
                if soup.find('div',{'class': 'productItemType1 cf offer'}):
                    for div in soup.find_all(
                        'div',{'class': 'productItemType1 cf offer'}):
                        # don't need %, just usual numeric price
                        if div.find('p',{'class': 'newPrice'}):
                            product = []
                            product.append(web_site)
                            product.append(store_dict[t])
                            product.append(date_str)
                            product.append('https://popusti.njuskalo.hr' 
                                + div.find('a')['href'])
                            product.append(k[0])
                            product.append(str(div.find('a')['href'].split('-')[-1]))
                            product.append(div.find('div',{'class': 'infoCont'})
                                .find('a').get_text().strip())
                            product.append(float(div.find('p',{'class': 'newPrice'})
                                .get_text().strip().split(' ')[0]
                                .replace(".","").replace(",",".")))
                            result.append(product)
                            
        time.sleep(1)

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()