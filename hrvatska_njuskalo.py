import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

STORE_DICT = {
    'Boso': 10,
    'Interspar': 11,
    'NTL': 14,
    'SPAR': 16,
    'Studenac': 17}

STORE_LIST = list(STORE_DICT.keys())

CATEGORIES = [
    ['Kandit','slatkisi-grickalice'],
    ['Saponia','paste-za-zube'],
    ['Saponia','deterdzenti-za-rublje'],
    ['Saponia','omeksivaci-za-rublje'],
    ['Saponia','deterdzenti-za-posude'],
    ['Saponia','sredstva-za-ciscenje']
]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    products = []
    start_time = time.perf_counter()

    for t in STORE_LIST:
        for category in CATEGORIES:
            print(category)
            category_name, category_url = category
            
            for x in range(1,101):   
                url=f'https://popusti.njuskalo.hr/trgovina/{t}/{category_url}?page={x}&ajax=1&xitiIndex=16'
                web_page = fake_headers(url, 0)
                soup = BeautifulSoup(web_page, 'html.parser')
                
                # don't know exact page numbers, so i'm checking if element exist
                if soup.find('div',{'class': 'productItemType1 cf offer'}):
                    for div in soup.find_all('div',{'class': 'productItemType1 cf offer'}):
                        # don't need %, just usual numeric price
                        if div.find('p',{'class': 'newPrice'}):
                            product = [
                                STORE_DICT[t],  # store
                                str(date.today()),  # date
                                f'https://popusti.njuskalo.hr{div.find("a")["href"]}',
                                category_name,
                                str(div.find('a')['href'].split('-')[-1]),  # code
                                div.find('div',{'class': 'infoCont'}).find('a').get_text().strip(), # name
                                float(div.find('p',{'class': 'newPrice'}).get_text().strip().split(' ')[0]  # price
                                    .replace(".","").replace(",","."))
                            ]
                            price = product [7]
                            if price > 0:
                                products.append(product)
                else:
                    break
                            
        time.sleep(1)

    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()