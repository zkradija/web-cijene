import requests
import time
from datetime import date
import pyodbc as odbc
import config

kat = [ ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471252&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723560399'],
        ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471257&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723765060'],
        ['Kandit', 'https://www.konzumshop.ba/v2/categories/5471244/products?filter%5Bsubcategory_ids%5D%5B%5D=5471265&filter%5Bshow%5D=all&filter%5Bsort%5D=nameAsc&filter%5Bsort_field%5D=name&page=1&per_page=1000&time=1685723789845'],
        ['Saponia', 'https://www.konzumshop.ba/v2/categories/5472087/products?filter%5Bshow%5D=all&filter%5Bsort_field%5D=soldStatistics&filter%5Bsort%5D=soldStatistics&page=1&per_page=1000&time=1685723815904'],
        ['Saponia', 'https://www.konzumshop.ba/v2/categories/5471607/products?filter%5Bshow%5D=all&filter%5Bsort_field%5D=soldStatistics&filter%5Bsort%5D=soldStatistics&page=1&per_page=1000&time=1685723857930'],
        ]

def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    result = []

    web_mjesto=11
    trgovina = 21
    datum = str(date.today())

    pocetak_vrijeme = time.time()
    
    s = requests.Session()

    for k in kat:
        r = s.request('GET', k[1], headers=headers)
        data = r.json()

        for d in data['products']:
            product = []
            product.append(web_mjesto)
            product.append(trgovina)
            product.append(datum)
            product.append('https://www.konzumshop.ba' + d['product_path'])
            product.append(k[0])
            product.append(d['code'])
            product.append(d['name'])
            product.append(float(d['price']['amount'])/100)
            product.append(d['barcodes'][0])
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
