from bs4 import BeautifulSoup
import requests
import time
from datetime import date
import pyodbc as odbc
import sys
import config_test

kat =   [['Kandit','https://voli.me/kategorije/52'],
        ['Kandit','https://voli.me/kategorije/53'],
        ['Kandit','https://voli.me/kategorije/54'],
        ['Kandit','https://voli.me/kategorije/59'],
        ['Saponia','https://voli.me/kategorije/188'],
        ['Saponia','https://voli.me/kategorije/189'],
        ['Saponia','https://voli.me/kategorije/213'],
        ['Saponia','https://voli.me/kategorije/214'],
        ['Saponia','https://voli.me/kategorije/216'],
        ['Saponia','https://voli.me/kategorije/217'],
        ['Saponia','https://voli.me/kategorije/218'],
        ['Saponia','https://voli.me/kategorije/220'],
        ['Saponia','https://voli.me/kategorije/222'],
        ['Saponia','https://voli.me/kategorije/223'],
        ['Saponia','https://voli.me/kategorije/224']]




def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    start_time = time.time()
    s = requests.Session()

    result = []
    web_site=10
    trgovina=20
    date_str = str(date.today())
    start_time = time.time()

    product_dict = {}
    for k in kat:
        print(k)
        response = s.get(k[1], headers=headers)
        web_page = response.text
        soup = BeautifulSoup(web_page, 'html.parser')

        for div in soup.find_all('div', {'class': 'card-body p-3'}):
            if str(div.find('div', {'class': 'card-text'}).find('a')['href']).split('/')[-1] in product_dict:
                break
            product = []
            product.append(web_site)
            product.append(trgovina)
            product.append(date_str)
            product.append(str(div.find('div', {'class': 'card-text'}).find('a')['href']))
            product.append(k[0])
            product.append(str(div.find('div', {'class': 'card-text'}).find('a')['href']).split('/')[-1])
            product.append(div.find('div', {'class': 'card-text'}).get('title').strip())
            if div.find('div',{'class':'product-price pl-special text-primary'}):
                product.append(float(div.find('div',{'class': 'price-wrapper'}).find('div',{'class': 'product-price pl-special text-primary'}).get_text().strip().split('€')[0].replace(',','')))
            else: 
                product.append(float(div.find('div',{'class': 'price-wrapper'}).find('div',{'class': 'product-price text-secondary'}).get_text().strip().split('€')[0].replace(',','')))
            product_dict[product[5]]=1

            result.append(product)
        time.sleep(1)

    # insert u SQL bazu    
    server = config_test.server
    database = config_test.database
    username = config_test.username
    password = config_test.password

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
        insert into cijene (WebMjestoId,TrgovinaId,date_str,poveznica,kategorija,sifra,naziv,cijena) 
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

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)


if __name__ == "__main__":
    main()        