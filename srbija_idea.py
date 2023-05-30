from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
from datetime import date
import pyodbc as odbc
import sys

# internet stranica online.idea.rs

kat =   [['Kandit','https://online.idea.rs/#!/categories/60014036/mlecna-cokolada','60014036'],
        ['Kandit','https://online.idea.rs/#!/categories/60014037/cokolada-za-kuvanje','60014037'],
        ['Kandit','https://online.idea.rs/#!/categories/60014026/bombonjera','60014026'],
        ['Kandit','https://online.idea.rs/#!/categories/60014056/barovi','60014056'],
        ['Kandit','https://online.idea.rs/#!/categories/60014028/bombone-i-zvake','60014028'],
        ['Saponia','https://online.idea.rs/#!/categories/60016209/praskasti-deterdzent','60016209'],
        ['Saponia','https://online.idea.rs/#!/categories/60016210/tecni-deterdzent','60016210'],
        ['Saponia','https://online.idea.rs/#!/categories/60016211/kapsule','60016211'],
        ['Saponia','https://online.idea.rs/#!/categories/60007776/omeksivaci-i-oplemenjivaci-vesa','60007776'],
        ['Saponia','https://online.idea.rs/#!/categories/60016205/rucno-pranje','60016205'],
        ['Saponia','https://online.idea.rs/#!/categories/60016218/za-ciscenje-kuhinje','60016218'],
        ['Saponia','https://online.idea.rs/#!/categories/60016219/za-ciscenje-kupatila','60016219'],
        ['Saponia','https://online.idea.rs/#!/categories/60016220/za-ciscenje-podova-namestaja-stakla','60016220'],
        ['Saponia','https://online.idea.rs/#!/categories/60016221/za-dezinfekciju-eco-i-univerzalna','60016221'],
        ['Saponia','https://online.idea.rs/#!/categories/60007873/paste','60007873']]



def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    web_mjesto=4
    trgovina = 3
    datum = str(date.today())

    pocetak_vrijeme = time.time()
    s = requests.Session()

    result=[]

    for k in kat:
        url = "https://online.idea.rs/v2/categories/" + str(k[2]) + "/products"
        querystring = {"per_page":"1000","page":"1","filter^%^5Bsort^%^5D":"soldStatisticsDesc"}
        r = requests.request('GET', url, params=querystring)
        data = r.json()
        for d in data['products']:
            product = []
            product.append(web_mjesto)
            product.append(trgovina)
            product.append(datum)
            product.append('https://online.idea.rs/#!' + d['product_path'])
            product.append(k[0])
            product.append(d['id'])
            product.append(d['name'])
            product.append(float(float(d['price']['amount']/100)))
            product.append(d['barcodes'][0][:13])
            result.append(product)
        time.sleep(1)
    
    # insert u SQL bazu    
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
