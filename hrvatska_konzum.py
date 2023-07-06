import time
from datetime import date, datetime

from bs4 import BeautifulSoup, SoupStrainer

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit', 'https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/cokolade'],
    ['Kandit', 'https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/bombonijere'],
    ['Kandit', 'https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/snackovi'],
    ['Kandit', 'https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/bomboni-lizalice-zvakace-gume'],
    ['Kandit', 'https://www.konzum.hr/web/t/kategorije/zdravi-kutak/slatkisi-i-grickalice/cokolade-i-bomboni'],
    ['Koestlin', 'https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/grickalice/stapici-pereci-krekeri-kokice'],
    ['Koestlin', 'https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/keksi'],
    ['Saponia', 'https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-rublja/deterdzenti'],
    ['Saponia', 'https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-rublja/omeksivaci'],
    ['Saponia', 'https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-posuda'],
    ['Saponia', 'https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/sredstva-za-ciscenje'],
    ['Saponia', 'https://www.konzum.hr/web/t/kategorije/njega-i-higijena/njega-zubi/paste']
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()
    
    for category in CATEGORIES:
        category_name, url = category
        for x in range(1,101):   # expecting less then 1000 products / category
            print(f'{category} --> page {x}')
            web_page = fake_headers(f'{url}?page={x}&per_page=100&sort%5B%5D=', 0)
            only_article_tags = SoupStrainer('article')  # i'm interested only in article tags
            soup = BeautifulSoup(web_page, 'html.parser', parse_only=only_article_tags)
            
            if soup.find('article'):
                for article in soup.find_all('article'):
                    code = article.div.attrs['data-ga-id']
                    if code in unique_codes:
                        pass
                    else:
                        product = [
                            1,  # store
                            str(date.today()),  # date
                            f'https://konzum.hr{article.find("a", {"class": "link-to-product"})["href"]}',
                            category_name,
                            code,
                            str(article.div.attrs['data-ga-name']),     # name
                            float(article.div.attrs['data-ga-price']    # price
                                .replace(' €', '')
                                .replace('.', '')
                                .replace(',', '.'))
                        ]
                        price = product[7]
                        if price > 0:  # Check if price > 0
                            unique_codes.add(product[5])
                            products.append(product)
            else:
                break
            time.sleep(1)
                

    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()