from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import pyodbc as odbc
import sys
import config


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
    
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    result = []

    web_mjesto=6
    trgovina = 5
    datum = str(date.today())

    pocetak_vrijeme = time.time()
    s = requests.Session()

    for k in kat:
        response = s.get(k[1], headers=headers)
        web_page = response.text
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'artikli_pojedinacan_artikal'}):
            product = []
            product.append(web_mjesto)
            product.append(trgovina)
            product.append(datum)
            product.append(str(div.find('div', {'class': 'artikli_pojedinacan_slika_okvir'}).find('a')['href']))
            product.append(k[0])
            product.append(div.find('div', {'class': 'artikli_pojedinacan_slika_okvir'}).find('a')['href'].split('/')[3])
            product.append(div.find('div',{'class':'artikli_pojedinacan_naziv'}).get_text().strip())
            product.append(float(div.find('div',{'class': 'artikli_pojedinacan_cena'}).get_text().replace('din/kom','')))
            result.append(product)
        time.sleep(1)

    # insert u SQL bazu    
    server = config.server
    database = config.database
    username = config.username
    password = config.password

    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = odbc.connect(conn_str)
    cursor = conn.cursor()

    try:
        conn = odbc.connect(conn_str)
    except Exception as e:
        print(e)
        print('Task is terminated')
        sys.exit
    else:
        cursor = conn.cursor()

    insert_statement = '''
        insert into cijene (WebMjestoId,TrgovinaId,datum,poveznica,kategorija,sifra,naziv,cijena) 
        values (?,?,?,?,?,?,?,?)
        '''

    try:
        for d in result:
            cursor.execute(insert_statement, d)
    except Exception as e:
        cursor.rollback()
        print(e.value)
        print('Transaction rolled back')
    else:
        print(f'{len(result)} records inserted successfully')
        cursor.commit()
        cursor.close()

    kraj_vrijeme = time.time()
    ukupno_vrijeme = kraj_vrijeme - pocetak_vrijeme
    print(ukupno_vrijeme)


if __name__ == "__main__":
    main()