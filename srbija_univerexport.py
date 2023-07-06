import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit','https://elakolije.rs/70004/polica/cokoladni-program'],
    ['Kandit','https://elakolije.rs/7000120/polica/bombone'],
    ['Kandit','https://elakolije.rs/70005/polica/bombonjere-praline-i-drazeje'],
    ['Saponia','https://elakolije.rs/a000110/polica/paste-za-zube'],
    ['Saponia','https://elakolije.rs/b0001/polica/deterdzenti-i-sredstva-za-ves'],
    ['Saponia','https://elakolije.rs/b0002/polica/odrzavanje-kuhinje'],
    ['Saponia','https://elakolije.rs/b0003/polica/odrzavanje-podova-i-namestaja-'],
    ['Saponia','https://elakolije.rs/b0004/polica/odrzavanje-kupatila-'],
    ['Saponia','https://elakolije.rs/b000525/polica/za-odrzavanje-domacinstva']
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()  # Set to store unique product codes
    
    for category in CATEGORIES:
        print(category)
        category_name, url = category
        web_page = fake_headers(url, 0)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'artikli_pojedinacan_artikal'}):
            product_url = div.find('div', {'class': 'artikli_pojedinacan_slika_okvir'}).find('a')['href']
            code = product_url.split('/')[3]
            if code not in unique_codes:
                product = [
                    5,  # store
                    str(date.today()),  # date
                    product_url,
                    category_name,
                    code,
                    div.find('div',{'class':'artikli_pojedinacan_naziv'}).get_text().strip(),   # name
                    float(div.find('div',{'class': 'artikli_pojedinacan_cena'}).get_text().replace('din/kom',''))
                ]
                price = product[7]            
                if price > 0:
                    unique_codes.add(code)
                    products.append(product)
        
        time.sleep(1)
    
    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()