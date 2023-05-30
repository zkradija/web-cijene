from bs4 import BeautifulSoup, SoupStrainer
import requests
import xlsxwriter
import time
from datetime import date
import pyodbc as odbc
import sys


# sa internet stranice https://Konzum.hr skinuti sve proizvode s pripadajućim cijenama
# cijene ću preuzeti sa stranice kategorija, jer tamo ima i cijena


kat =   [['Kandit','https://cenoteka.rs/proizvodi/slatkisi-i-grickalice/cokolade'],
         ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/deterdzent-za-posude'],
         ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/omeksivac-za-ves'],
         ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/praskasti-deterdzenti-za-ves']]


def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    result = []

    web_mjesto = 3
    datum = str(date.today())

    pocetak_vrijeme = time.time()
    s = requests.Session()

    for k in kat:
        response = s.get(k[1], headers=headers)
        web_page = response.text
        soup = BeautifulSoup(web_page, "html.parser")

        br_str = int(soup.find('ul', {'class':'pagination justify-content-center'}).find_all('li')[-2].find('a').get_text())

        for x in range (1, br_str + 1):
            response = s.get(k[1] + '?page=' + str(x), headers=headers)
            web_page = response.text
            soup = BeautifulSoup(web_page, "html.parser")

            for d in soup.find('div', {'id' : 'products'}).find_all('div'):
                if d.has_attr('data-product-id'):
                    #PL ovi znaju biti i pojedinačno i skupno prikazani. ako nema poveznice, ne zanimaju me (pojedinačno prikazani)
                    if d.find_all('div')[1].find('a'):
                        #IDEA
                        product = []                
                        product.append(web_mjesto)
                        product.append(3)
                        product.append(datum)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1].find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[0].get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        if product[7] != 0: result.append(product)
                        
                        #Maxi
                        product = []
                        product.append(web_mjesto)
                        product.append(4)
                        product.append(datum)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1].find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[1].get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        if product[7] != 0: result.append(product)

                        #Univerexport
                        product = []
                        product.append(web_mjesto)
                        product.append(5)
                        product.append(datum)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1].find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[2].get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        if product[7] != 0: result.append(product)

                        #Tempo
                        product = []
                        product.append(web_mjesto)
                        product.append(6)
                        product.append(datum)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1].find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[3].get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        if product[7] != 0: result.append(product)

                        #DIS Rakovica
                        product = []
                        product.append(web_mjesto)
                        product.append(7)
                        product.append(datum)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1].find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[4].get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        if product[7] != 0: result.append(product)

                        #Roda
                        product = []
                        product.append(web_mjesto)
                        product.append(8)
                        product.append(datum)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1].find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[5].get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        if product[7] != 0: result.append(product)

                        
                        #Lidl - ubacujem provjeru je li postoji zadnji stupac - trgovina Lidl
                        if len(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})) > 6:
                            product = []
                            product.append(web_mjesto)
                            product.append(9)
                            product.append(datum)
                            product.append('https://cenoteka.rs' + d.find_all('div')[1].find('a').get('href'))
                            product.append(k[0])
                            product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                            product.append(d.find_all('div')[1].get_text().strip())
                            product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[6].get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                            if product[7] != 0: result.append(product)

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
        insert into cijene (WebMjestoId,TrgovinaId,datum,poveznica,kategorija,sifra,naziv,cijena) 
        values (?,?,?,?,?,?,?,?)
        '''

    try:
        for d in result:
            # print(d)
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
