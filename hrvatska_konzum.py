from bs4 import BeautifulSoup, SoupStrainer
import requests
import time
from datetime import date
import pyodbc as odbc
import sys

# sa internet stranice https://Konzum.hr skinuti sve proizvode s pripadajućim cijenama
# cijene ću preuzeti sa stranice kategorija, jer tamo ima i cijena

kat =   [['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/cokolade'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/bombonijere'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/snackovi'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/bomboni-lizalice-zvakace-gume'],
        ['Kandit','https://www.konzum.hr/web/t/kategorije/zdravi-kutak/slatkisi-i-grickalice/cokolade-i-bomboni'],
        ['Koestlin','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/grickalice/stapici-pereci-krekeri-kokice'],
        ['Koestlin','https://www.konzum.hr/web/t/kategorije/slatkisi-i-grickalice/keksi'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-rublja/deterdzenti'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-rublja/omeksivaci'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/pranje-posuda'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/ciscenje-i-pospremanje/sredstva-za-ciscenje'],
        ['Saponia','https://www.konzum.hr/web/t/kategorije/njega-i-higijena/njega-zubi/paste']]

def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    data = []

    web_mjesto=1
    trgovina = 1
    datum = str(date.today())

    pocetak_vrijeme = time.time()
    s = requests.Session()

    for k in kat:
        response = s.get(k[1], headers=headers)
        web_page = response.text
        only_article_tags = SoupStrainer(
            "article"
        )  # i'm interested only in article tags
        soup = BeautifulSoup(web_page, "html.parser", parse_only=only_article_tags)

        for article in soup.find_all("article"):
            product = []
            if article is not None:
                product.append(web_mjesto)
                product.append(trgovina)
                product.append(datum)
                product.append(
                    "https://konzum.hr"
                    + str(article.find("a", {"class": "link-to-product"})["href"])
                )
                product.append(k[0])
                product.append(str(article.div.attrs["data-ga-id"]))
                product.append(str(article.div.attrs["data-ga-name"]))
                product.append(
                    float(
                        article.div.attrs["data-ga-price"]
                        .replace(" €", "")
                        .replace(",", ".")
                    )
                )
                data.append(product)
    
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
        for d in data:
            # print(d)
            cursor.execute(insert_statement, d)
    except Exception as e:
        cursor.rollback()
        print(e.value)
        print('Transaction rolled back')
    else:
        print(len(data))
        print('Record inserted successfully')
        cursor.commit()
        cursor.close()

    kraj_vrijeme = time.time()
    ukupno_vrijeme = kraj_vrijeme - pocetak_vrijeme
    print(ukupno_vrijeme)


if __name__ == "__main__":
    main()
