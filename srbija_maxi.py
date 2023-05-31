from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
from datetime import date
import pyodbc as odbc
import sys
import config


kat =   [['Kandit','Čokoladni proizvodi','0701'],
        ['Saponia', 'Sredstva za čišćenje i osveživači', '1305'],
        ['Saponia', 'Ručno pranje sudova', '130101'],
        ['Saponia', 'Deterdženti za veš i omekšivači', '1303'],
        ['Saponia', 'Paste za zube', '140101']]

def main():
    pocetak_vrijeme = time.time()
    s = requests.Session()
    result=[]

    web_mjesto = 5
    trgovina = 4
    datum = str(date.today())

    for k in kat:
        print(k[1])
        url_page_number = 'https://www.maxi.rs/api/v1/?operationName=GetCategoryProductSearch&variables=%7B%22lang%22%3A%22sr%22%2C%22searchQuery%22%3A%22%3Arelevance%22%2C%22sort%22%3A%22relevance%22%2C%22category%22%3A%22'+ str(k[2]) +'%22%2C%22pageNumber%22%3A0%2C%22pageSize%22%3A20%2C%22filterFlag%22%3Atrue%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2265b0b1aacb2caeea6468873e8f7fde0ef82ffb0c4f9c93583c41070fa1f13c82%22%7D%7D'
        r = s.get(url_page_number)
        page_number = int(r.json()['data']['categoryProductSearch']['pagination']['totalPages'])

        for x in range (0,page_number):
            url = 'https://www.maxi.rs/api/v1/?operationName=GetCategoryProductSearch&variables=%7B%22lang%22%3A%22sr%22%2C%22searchQuery%22%3A%22%3Arelevance%22%2C%22sort%22%3A%22relevance%22%2C%22category%22%3A%22' + str(k[2]) + '%22%2C%22pageNumber%22%3A' + str(x) + "%2C%22pageSize%22%3A20%2C%22filterFlag%22%3Atrue%2C%22plainChildCategories%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2265b0b1aacb2caeea6468873e8f7fde0ef82ffb0c4f9c93583c41070fa1f13c82%22%7D%7D"
            r = s.get(url)
            data = r.json()

            for d in data['data']['categoryProductSearch']['products']:
                product=[]
                product.append(web_mjesto)
                product.append(trgovina)
                product.append(datum)
                product.append('https://maxi.rs' + d['url'])
                product.append(k[0])
                product.append(d['code'])
                product.append(d['name'])
                product.append(float(d['price']['unitPrice']))
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

                

