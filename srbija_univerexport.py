import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql

kat = [ ['Kandit','https://elakolije.rs/70004/polica/cokoladni-program'],
        ['Kandit','https://elakolije.rs/7000120/polica/bombone'],
        ['Kandit','https://elakolije.rs/70005/polica/bombonjere-praline-i-drazeje'],
        ['Saponia','https://elakolije.rs/a000110/polica/paste-za-zube'],
        ['Saponia','https://elakolije.rs/b0001/polica/deterdzenti-i-sredstva-za-ves'],
        ['Saponia','https://elakolije.rs/b0002/polica/odrzavanje-kuhinje'],
        ['Saponia','https://elakolije.rs/b0003/polica/odrzavanje-podova-i-namestaja-'],
        ['Saponia','https://elakolije.rs/b0004/polica/odrzavanje-kupatila-'],
        ['Saponia','https://elakolije.rs/b000525/polica/za-odrzavanje-domacinstva']]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site = 6
    trgovina = 5
    date_str = str(date.today())
    start_time = time.time()

    for k in kat:
        print(k)
        web_page = fake_headers(k[1], indProxy)
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'artikli_pojedinacan_artikal'}):
            product = []
            product.append(web_site)
            product.append(trgovina)
            product.append(date_str)
            product.append(
                str(div.find('div', {'class': 'artikli_pojedinacan_slika_okvir'})
                .find('a')['href']))
            product.append(k[0])
            product.append(div.find('div', {'class': 'artikli_pojedinacan_slika_okvir'})
                           .find('a')['href'].split('/')[3])
            product.append(div.find('div',{'class':'artikli_pojedinacan_naziv'})
                           .get_text().strip())
            product.append(float(div.find('div',{'class': 'artikli_pojedinacan_cena'})
                                 .get_text().replace('din/kom','')))
            result.append(product)
            
        time.sleep(1)
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()