import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit','https://www.kaufland.hr/ponuda/ponuda-od-cetvrtka/ponuda-pregled.category=07_Kava__%C4%8Daj__slatki%C5%A1i__grickalice.html'],
    ['Saponia','https://www.kaufland.hr/ponuda/ponuda-od-cetvrtka/ponuda-pregled.category=09_Drogerija__hrana_za_ku%C4%87ne_ljubimce.html']
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.time()
    products = []
    unique_codes = set()

    for category in CATEGORIES:
        print(category)
        category_name, url = category
        web_page = fake_headers(url, 0)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'g-col o-overview-list__list-item'}):
            if div.find('a', {'class': 'm-offer-tile__link u-button--hover-children'}):
                product_href = div.find('a', {'class': 'm-offer-tile__link u-button--hover-children'})['href']
                code = product_href[-13:-5]
            # add product only if it has price, that way we skip div with ads
            # some products doesn't have name -> skip them!
            if (div.find('div', {'class': 'a-pricetag__price'}) and div.find('div',{'class': 'm-offer-tile__text'}).find('h5') 
                and code not in unique_codes):
                product = [
                    13,     # website
                    23,     # store
                    str(date.today()),      # date
                    f'https://www.kaufland.hr{product_href}',   # product url
                    category_name,                              
                    code,    # code
                ]
                if div.find('div',{'class': 'm-offer-tile__text'}).find('h4'):  # name
                    product.append(div.find('div',{'class': 'm-offer-tile__text'})
                                .find('h5')
                                .get_text()
                                .replace('\t','')
                                .strip()
                                + ' ' +
                                div.find('div',{'class': 'm-offer-tile__text'})
                                .find('h4')
                                .get_text()
                                .replace('\t','')
                                .strip()
                                )
                else:
                    product.append(div.find('div',{'class': 'm-offer-tile__text'})
                                .find('h5')
                                .get_text()
                                .replace('\t','')
                                .replace('-','')
                                .strip()
                                )
                product.append(
                    float(
                        div.find('div', {'class': 'a-pricetag__price'}).get_text()
                        .replace('€','')
                        .strip()
                    )
                )
                price = product[7]
                if price > 0:  # Check if price > 0
                    unique_codes.add(product[5])
                    products.append(product)
            

    # inserting data
    insert_sql(products)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()