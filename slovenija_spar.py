from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import pyodbc as odbc
import sys
import config


kat = [ ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-1&substringFilter=pos-visible%3A81701'],
        ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-2&substringFilter=pos-visible%3A81701'],
        ['Kandit','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path%3AS10-1-3&substringFilter=pos-visible%3A81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-2-1&substringFilter=pos-visible:81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-3&substringFilter=pos-visible:81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-1-1&substringFilter=pos-visible:81701'],
        ['Saponia','https://search-spar.spar-ics.com/fact-finder/rest/v4/search/products_lmos_si?query=*&q=*&page=1&hitsPerPage=1000&filter=category-path:S14-1-2&substringFilter=pos-visible:81701']]

def main():
    
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    result = []

    web_mjesto=8
    trgovina = 18
    datum = str(date.today())

    pocetak_vrijeme = time.time()
    s = requests.Session()

    for k in kat:
        r = s.get(k[1],headers=headers)
        data = r.json()

        for d in data['hits']:
            product=[]
            product.append(web_mjesto)
            product.append(trgovina)
            product.append(datum)
            product.append('www.spar.si/online' + d['masterValues']['url'])
            product.append(k[0])
            product.append(d['id'])
            product.append(d['masterValues']['title'] )
            product.append(float(d['masterValues']['best-price']))
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