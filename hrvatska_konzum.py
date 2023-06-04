import sys
import time
from datetime import date, datetime

from bs4 import BeautifulSoup, SoupStrainer

from headers import headers
from insert_sql import insert_sql

kat =   [['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/cokolade'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/bombonijere'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/snackovi'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/bomboni-lizalice-zvakace-gume'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/zdravi-kutak/slatkisi-i-grickalice/cokolade-i-bomboni'],
        ['Koestlin','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/grickalice/stapici-pereci-krekeri-kokice'],
        ['Koestlin','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/keksi'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-rublja/deterdzenti'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-rublja/omeksivaci'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-posuda'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/sredstva-za-ciscenje'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/njega-i-higijena/njega-zubi/paste']]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site=1
    store = 1
    date_str = str(date.today())

    # there is no barcode so im using dummy data
    barcode = ''
    start_time = time.time()

    for k in kat:
        print(k)
        web_page = headers(k[1], indProxy)
        only_article_tags = SoupStrainer(
            'article'
        )  # i'm interested only in article tags
        soup = BeautifulSoup(web_page, 'html.parser', parse_only=only_article_tags)

        for article in soup.find_all('article'):
            product = []
            if article is not None:
                product.append(web_site)
                product.append(store)
                product.append(date_str)
                product.append(
                    'https://konzum.hr'
                    + str(article.find('a', {'class': 'link-to-product'})['href'])
                )
                product.append(k[0])
                product.append(str(article.div.attrs['data-ga-id']))
                product.append(str(article.div.attrs['data-ga-name']))
                product.append(
                    float(
                        article.div.attrs['data-ga-price']
                        .replace(' €', '')
                        .replace('.', '')
                        .replace(',', '.')
                    )
                )
                product.append(barcode)
                result.append(product)
                

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()