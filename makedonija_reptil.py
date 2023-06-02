from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import pyodbc as odbc
import sys
import config
import cyrtranslit

kat =   [ 
        ['Kandit', 'https://marketonline.mk/product-category/%D1%85%D1%80%D0%B0%D0%BD%D0%B0/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%B4%D0%B5%D1%81%D0%B5%D1%80%D1%82%D0%B8-%D0%B8-%D0%B3%D1%80%D0%B8%D1%86%D0%BA%D0%B8/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%BA%D0%B0%D0%BA%D0%B0%D0%BE/?per_page=500'],
        ['Kandit', 'https://marketonline.mk/product-category/%D1%85%D1%80%D0%B0%D0%BD%D0%B0/%D1%87%D0%BE%D0%BA%D0%BE%D0%BB%D0%B0%D0%B4%D0%B8-%D0%B4%D0%B5%D1%81%D0%B5%D1%80%D1%82%D0%B8-%D0%B8-%D0%B3%D1%80%D0%B8%D1%86%D0%BA%D0%B8/%D0%BA%D0%BE%D0%BD%D0%B4%D0%B8%D1%82%D0%BE%D1%80%D1%81%D0%BA%D0%B8-%D0%BF%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%B4%D0%B8/%D0%B1%D0%BE%D0%BD%D0%B1%D0%BE%D0%BD%D0%B8-%D1%82%D0%B2%D1%80%D0%B4%D0%B8/?per_page=500'],
        ['Saponia', 'https://marketonline.mk/product-category/%D0%B4%D0%BE%D0%BC%D0%B0%D1%9C%D0%B8%D0%BD%D1%81%D1%82%D0%B2%D0%BE-%D0%B4%D0%BE%D0%BC%D0%B0%D1%9C%D0%B8%D0%BD%D1%81%D1%82%D0%B2%D0%BE/%D0%B4%D0%B5%D1%82%D0%B5%D1%80%D0%B3%D0%B5%D0%BD%D1%82%D0%B8-%D0%BE%D0%BC%D0%B5%D0%BA%D0%BD%D1%83%D0%B2%D0%B0%D1%87%D0%B8/?per_page=500'],
        ]

def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    result = []

    web_mjesto=12
    trgovina = 22
    datum = str(date.today())

    pocetak_vrijeme = time.time()
    s = requests.Session()

    def starts_with_my_class(class_name):
        return class_name and class_name.startswith('product-grid-item product wd-hover-standard')
    
    for k in kat:
        response = s.get(k[1], headers=headers)
        web_page = response.text

        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', class_=starts_with_my_class):
            product = []
            product.append(web_mjesto)
            product.append(trgovina)
            product.append(datum)
            product.append(div.find('a')['href'])
            product.append(k[0])
            product.append(div.attrs['data-id'])
            latin_name = cyrtranslit.to_latin(div.find('h3', {'class': 'wd-entities-title'}).get_text(), 'mk')
            product.append(latin_name)
            product.append(
                float(
                    div.find('span', {'class': 'woocommerce-Price-amount amount'}).get_text()
                    .replace('\xa0ден','')
                    .replace('.', '')
                    .replace(',', '.')
                )
            )
            result.append(product)
            print(product)
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
        for r in result:
            # print(d)
            cursor.execute(insert_statement, r)
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
