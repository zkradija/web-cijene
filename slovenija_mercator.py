from bs4 import BeautifulSoup, SoupStrainer
import requests
import xlsxwriter
import time
from datetime import date
import pyodbc as odbc
import sys
import pandas as pd

# internet stranica https://trgovina.mercator.si


def main():


    drzava = 'Slovenija'
    trgovina = 'Mercator'
    datum = str(date.today())
    pocetak_vrijeme = time.time()

    result = []

    # Kandit
    for x in range (0,10):
        y = x * 100
        url = f'https://trgovina.mercator.si/market/products/browseProducts/getProducts?limit=100&offset={x}&filterData%5Bcategories%5D=14535711&filterData%5Boffset%5D=8&from={y}&_=1684918912105'
        r = requests.request('GET', url)
        data = r.json()

        for d in data:
            product = []
            if 'data' in d: 
                product.append(drzava)
                product.append(trgovina)
                product.append(datum)
                product.append('https://trgovina.mercator.si' + d['url'].replace('\\',''))
                product.append('Kandit')
                product.append(d['data']['code'])
                product.append(d['data']['name'])
                product.append(d['data']['current_price'])
                product.append(d['data']['gtins'][0]['gtin'])
                result.append(product)
        time.sleep(1)

    # Saponia
    for x in range (0,7):
        y = x * 100
        url = f'https://trgovina.mercator.si/market/products/browseProducts/getProducts?limit=100&offset={x}&filterData%5Bcategories%5D=14535906&filterData%5Boffset%5D=6&from={y}&_=168493248856'
        r = requests.request('GET', url)
        data = r.json()

        for d in data:
            product = []
            if 'data' in d: 
                product.append(drzava)
                product.append(trgovina)
                product.append(datum)
                product.append('https://trgovina.mercator.si' + d['url'].replace('\\',''))
                product.append('Saponia')
                product.append(d['data']['code'])
                product.append(d['data']['name'])
                product.append(d['data']['current_price'])
                product.append(d['data']['gtins'][0]['gtin'])
                result.append(product)
        time.sleep(1)



    # prvo ubacujem u SQL bazu
    server = 'ZKradija\MSSQLSERVER22'
    database = 'WebCijene'
    username = 'webcijene'
    password = 'webcijene123!'

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
        insert into cijene (drzava,trgovina,datum,poveznica, kategorija, sifra, naziv, cijena, gtin_kom) 
        values (?,?,?,?,?,?,?,?,?)
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
        print('Record inserted successfully')
        cursor.commit()
        cursor.close()
  

    kraj_vrijeme = time.time()
    ukupno_vrijeme = kraj_vrijeme - pocetak_vrijeme
    print(ukupno_vrijeme)


if __name__ == "__main__":
    main()
