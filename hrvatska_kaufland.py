import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

kat =   [['Kandit','https://www.kaufland.hr/ponuda/ponuda-od-cetvrtka/ponuda-pregled.category=07_Kava__%C4%8Daj__slatki%C5%A1i__grickalice.html'],
        ['Saponia','https://www.kaufland.hr/ponuda/ponuda-od-cetvrtka/ponuda-pregled.category=09_Drogerija__hrana_za_ku%C4%87ne_ljubimce.html']]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site=13
    store = 23
    date_str = str(date.today())

    # there is no barcode so im using dummy data
    barcode = ''
    start_time = time.time()

    for k in kat:
        print(k)
        web_page = fake_headers(k[1], indProxy)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'g-col o-overview-list__list-item'}):
            # add product only if it has price, that way we skip div with ads
            # some products doesn't have name -> skip them!
            if (div.find('div', {'class': 'a-pricetag__price'}) 
                    and div.find('div',{'class': 'm-offer-tile__text'}).find('h5')):
                product = []
                product.append(web_site)
                product.append(store)
                product.append(date_str)
                product.append(
                    'https://www.kaufland.hr' 
                        + str(div.find('a', {'class': 
                        'm-offer-tile__link u-button--hover-children'})['href'])
                )
                product.append(k[0])
                product.append(str(div.find('a', {'class': 
                    'm-offer-tile__link u-button--hover-children'})['href'][-13:-5]))
                if div.find('div',{'class': 'm-offer-tile__text'}).find('h4'):
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
                product.append(barcode)
                result.append(product)
            

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == '__main__':
    main()