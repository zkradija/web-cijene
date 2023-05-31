import requests
import time
from datetime import date
import pyodbc as odbc
import config


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    web_mjesto = 2
    trgovina = 2
    datum = str(date.today())
    pocetak_vrijeme = time.time()

    result = []

    # Kandit
    for x in range (0,10):
        y = x * 100
        url = f'https://trgovina.mercator.si/market/products/browseProducts/getProducts?limit=100&offset={x}&filterData%5Bcategories%5D=14535711&filterData%5Boffset%5D=8&from={y}&_=1684918912105'
        r = requests.request('GET', url, headers=headers)
        data = r.json()

        for d in data:
            product = []
            if 'data' in d: 
                product.append(web_mjesto)
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
        r = requests.request('GET', url, headers=headers)
        data = r.json()

        for d in data:
            product = []
            if 'data' in d: 
                product.append(web_mjesto)
                product.append(trgovina)
                product.append(datum)
                product.append('https://trgovina.mercator.si' + d['url'].replace('\\',''))
                product.append('Saponia')
                product.append(d['data']['code'])
                product.append(d['data']['name'])
                product.append(d['data']['current_price'])
                product.append(d['data']['gtins'][0]['gtin'][:13])
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
    else:
        cursor = conn.cursor()

    insert_statement = '''
        insert into cijene (WebMjestoId,TrgovinaId,datum,poveznica,kategorija,sifra,naziv,cijena,GtinKom) 
        values (?,?,?,?,?,?,?,?,?)
        '''

    try:
        for r in result:
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
