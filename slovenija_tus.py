from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pyodbc as odbc
import sys
import config

kat =   [['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Čokolade',0],
         ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Bonboni',0],
         ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Bonboniere',1],
         ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Čokoladne rezine',1],
         ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Čokoladne banane',1],
         ['Saponia','https://hitrinakup.com/kategorije/Osebna%20nega/Nega%20ust%20in%20zob','Zobne paste',0],
         ['Saponia','https://hitrinakup.com/kategorije/Osebna%20nega/Nega%20ust%20in%20zob','Zobne paste za otroke',0],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom','Mehčalci',0],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom','Tekoči pralni praški',0],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom','Pralni praški v kapsulah',1],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom','Trdi pralni praški',1],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/Detergetni%20za%20pomivanje%20posode?categoryName=Dom','Strojno pomivanje posode',0],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/Detergetni%20za%20pomivanje%20posode?categoryName=Dom','Ročno pomivanje posode',0],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom','Druga čistila',0],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom','Čistila za kuhinjo',0],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom','Univerzalna čistila',1],
         ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom','Čistila za steklo',1]]


def main():
    result = []
    time_sleep = 3
    web_mjesto=9
    trgovina = 19
    datum = str(date.today())
    pocetak_vrijeme = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path = r'./chromedriver', options=options)


    def scroll():
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(time_sleep)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def parse(url,subcategory):
        driver.get(url)
        # driver.maximize_window()
        driver.set_window_size(1920, 1080)
        time.sleep(time_sleep)
        if k[3] == 1 :
            subFilter_checkbox = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'show-more-sub')))
            subFilter_checkbox.click()
            time.sleep(1)
        filter_checkbox = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, subcategory)))
        filter_checkbox.click()
        time.sleep(time_sleep)
        scroll()
        
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'html.parser')

        for a in soup.find_all('a', {'class': 'HorizontalScrollingItems_itemCardWrapper__177cw'}):
            product = []
            product.append(web_mjesto)
            product.append(trgovina)
            product.append(datum)
            product.append('https://hitrinakup.com' + str(a['href']))
            product.append(k[0])
            product.append(str(a['href']).split('/')[2])
            product.append(a.find('div', {'class': 'HorizontalScrollingItems_itemCardDetailsContainer__cfMAa'}).find('div', {'class': 'HorizontalScrollingItems_itemProductTitle__GxcAp'}).get_text().strip())
            product.append(a.find('span', {'id': 'price'}).get_text().replace('\xa0€ / kos','').strip().replace('.','').replace(',','.'))
            result.append(product)
    for k in kat:
        print(k)
        parse(k[1],k[2])

    driver.quit()

    #print(result)

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


if __name__ == '__main__':
    main()