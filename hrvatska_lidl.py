import json
import time
from datetime import date, datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import chromedriver_autoinstaller
from webdriver_auto_update import check_driver

from fake_headers import fake_headers
from insert_sql import insert_sql

def main():
    chromedriver_autoinstaller.install()
    # Pass in the folder used for storing/downloading chromedriver
    check_driver('D:/Git/web-cijene/venv/Lib/site-packages/chromedriver_autoinstaller/')

    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()

    time_sleep = 3

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1980,1020")
    options.add_argument('--headless')
#    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

    url = 'https://www.lidl.hr/letak'
    
    driver.get(url)
    
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'cookie-alert-extended-button'))).click()
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'productgrid__list>li:first-child')))
    url = driver.find_element(By.CLASS_NAME, 'productgrid__list>li:first-child').find_element(By.CLASS_NAME, 'link').get_attribute('href')
    driver.quit()
    
    flyer_identifier = url.split('/')[5]
    url_json = f'https://endpoints.leaflets.schwarz/v4/flyer?flyer_identifier={flyer_identifier}&region_id=0&region_code=0'
    
    response = fake_headers(url_json, 0)
    data = json.loads(response)

    
    if data['flyer']['products']:
        for product in data['flyer']['products'].values():
            code = product['productId']
            price = float(product['price'])
            if code not in unique_codes and price > 0:
            # Only add the product if its code is not already in the set
                products.append([
                    23, # web_site
                    13, # store
                    str(date.today()),  # date_str
                    product['url'].split('?')[0],
                    'Sve',              # category_name
                    code,
                    product['title'],   # name
                    price,
                ])
                unique_codes.add(code)
        
    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()
    
