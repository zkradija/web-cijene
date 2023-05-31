from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import pyodbc as odbc
import sys
import config


trgovina_dict = {
    'Boso': 10,
    'Interspar': 11,
    'Kaufland': 12,
    'Lidl': 13,
    'NTL': 14,
    'Plodine': 15,
    'SPAR': 16,
    'Studenac': 17}

trgovina_list = list(trgovina_dict.keys())

kat =   [['Kandit','slatkisi-grickalice'],
        ['Saponia','paste-za-zube'],
        ['Saponia','deterdzenti-za-rublje'],
        ['Saponia','omeksivaci-za-rublje'],
        ['Saponia','deterdzenti-za-posude'],
        ['Saponia','sredstva-za-ciscenje']]



def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    result = []
    web_mjesto = 7

    datum = str(date.today())
    pocetak_vrijeme = time.time()
    s = requests.Session()

    for t in trgovina_list:
        for k in kat:
            print(f'{t} / {k[1]}')
            # nema više od 2 stranice , po trgovini / kategoriji, a kamoli 10
            for x in range(1,11):   
                url=f'https://popusti.njuskalo.hr/trgovina/{t}/{k[1]}?page={x}&ajax=1&xitiIndex=16'
                response = s.get(url, headers=headers)
                web_page = response.text
                soup = BeautifulSoup(web_page, 'html.parser')
                # ne znam koliko ima stranica pa moram provjeravati je li postoje traženi elementi
                if soup.find('div',{'class': 'productItemType1 cf offer'}):
                    for div in soup.find_all('div',{'class': 'productItemType1 cf offer'}):
                        # ne zanimaju me postotna sniženja pa radim filter za cijene
                        if div.find('p',{'class': 'newPrice'}):
                            product = []
                            product.append(web_mjesto)
                            product.append(trgovina_dict[t])
                            product.append(datum)
                            product.append('https://popusti.njuskalo.hr/' + div.find('a')['href'])
                            product.append(k[0])
                            product.append(str(div.find('a')['href'].split('-')[-1]))
                            product.append(div.find('div',{'class': 'infoCont'}).find('a').get_text().strip())
                            product.append(float(div.find('p',{'class': 'newPrice'}).get_text().strip().split(' ')[0].replace(".","").replace(",",".")))
                            result.append(product)
                            print(str(x) + ' ' + str(product))
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