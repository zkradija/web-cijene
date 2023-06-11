import time
from datetime import date, datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Čokolade', 0],
    ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Bonboni', 0],
    ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki','Bonboniere', 1],
    ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki', 'Čokoladne rezine', 1],
    ['Kandit','https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki', 'Čokoladne banane', 1],
    ['Saponia','https://hitrinakup.com/kategorije/Osebna%20nega/Nega%20ust%20in%20zob', 'Zobne paste', 0],
    ['Saponia','https://hitrinakup.com/kategorije/Osebna%20nega/Nega%20ust%20in%20zob', 'Zobne paste za otroke', 0],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom', 'Mehčalci', 0],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom', 'Tekoči pralni praški',0],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom', 'Pralni praški v kapsulah', 1],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/Pranje%20perila?categoryName=Dom', 'Trdi pralni praški', 1],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/Detergetni%20za%20pomivanje%20posode?categoryName=Dom', 'Strojno pomivanje posode', 0],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/Detergetni%20za%20pomivanje%20posode?categoryName=Dom', 'Ročno pomivanje posode', 0],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom', 'Druga čistila', 0],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom', 'Čistila za kuhinjo', 0],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom', 'Univerzalna čistila', 1],
    ['Saponia','https://hitrinakup.com/kategorije/Dom/%C4%8Cistila?categoryName=Dom', 'Čistila za steklo',1]
]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.time()
    products = []
    unique_codes = set()

    time_sleep = 3

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

    def parse(url,subcategory, subFilter):
        driver.get(url)
        # driver.maximize_window()
        driver.set_window_size(1920, 1080)
        time.sleep(time_sleep)
        if subFilter == 1 :
            subFilter_checkbox = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'show-more-sub')))
            subFilter_checkbox.click()
            time.sleep(1)
        filter_checkbox = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, subcategory)))
        filter_checkbox.click()
        time.sleep(time_sleep)
        scroll()
        
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'html.parser')

        for a in soup.find_all('a', {'class': 'HorizontalScrollingItems_itemCardWrapper__177cw'}):
            code = str(a['href']).split('/')[2]
            product = [
                9,      # website
                19,     # store
                str(date.today()),  # date
                f'https://hitrinakup.com{a["href"]}',   # product_url
                category_name,
                code,
                a.find('div', {'class': 'HorizontalScrollingItems_itemCardDetailsContainer__cfMAa'})
                    .find('div', {'class': 'HorizontalScrollingItems_itemProductTitle__GxcAp'})
                    .get_text().strip(),    # name
                float(a.find('span', {'id': 'price'}).get_text().replace('\xa0€ / kos','')
                    .strip().replace('.','').replace(',','.'))   # price
                ]
            price = product[7]
            if price > 0:
                unique_codes.add(code)
                products.append(product)
            
    for category in CATEGORIES:
        print(category)
        category_name, url, subcategory, subFilter = category
        parse(url, subcategory, subFilter)

    driver.quit()

    # inserting data
    insert_sql(products)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()