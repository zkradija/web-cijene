import json
import time
from datetime import date, datetime

from selenium import webdriver
from selenium.webdriver.common.by import By


from fake_headers import fake_headers
from insert_sql import insert_sql


kat =   [
        ['Kandit','https://ponuda.metro-cc.hr/explore.articlesearch.v1/search?storeId=00010&language=hr-HR&country=HR&query=*&rows=1000&page=1&filter=category%3A12.-slatko-slano%2F%C4%8Dokolade-praline&facets=true&categories=true',
            'https://ponuda.metro-cc.hr/shop/category/12.-slatko-slano/%C4%8Dokolade-praline'],
        ['Kandt', 'https://ponuda.metro-cc.hr/explore.articlesearch.v1/search?storeId=00010&language=hr-HR&country=HR&query=*&rows=1000&page=1&filter=category%3A12.-slatko-slano%2Fbomboni-karamele-lizalice-%C5%BEele&facets=true&categories=true',
            'https://ponuda.metro-cc.hr/shop/category/12.-slatko-slano/bomboni-karamele-lizalice-%C5%BEele'],
        ['Koestlin', 'https://ponuda.metro-cc.hr/explore.articlesearch.v1/search?storeId=00010&language=hr-HR&country=HR&query=*&rows=1000&page=1&filter=category%3A12.-slatko-slano%2Fkeksi-kola%C4%8Di-oblatne&facets=true&categories=true',
            'https://ponuda.metro-cc.hr/shop/category/12.-slatko-slano/keksi-kola%C4%8Di-oblatne'],
        ['Koestlin', 'https://ponuda.metro-cc.hr/explore.articlesearch.v1/search?storeId=00010&language=hr-HR&country=HR&query=*&rows=1000&page=1&filter=category%3A12.-slatko-slano%2Fgrickalice-kokice&facets=true&categories=true',
            'https://ponuda.metro-cc.hr/shop/category/12.-slatko-slano/grickalice-kokice'],
        ['Saponia', 'https://ponuda.metro-cc.hr/explore.articlesearch.v1/search?storeId=00010&language=hr-HR&country=HR&query=*&rows=1000&page=1&filter=category%3A15.-deterd%C5%BEenti&facets=true&categories=true',
            'https://ponuda.metro-cc.hr/shop/category/15.-deterd%C5%BEenti']
         ]




def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')

    result=[]
    indProxy = 0
    web_site = 20
    store = 30
    date_str = str(date.today())
    barcode = ''
    start_time = time.time()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path = r'./chromedriver', options=options)

    driver.get('https://ponuda.metro-cc.hr/')
    time.sleep(7)

    # get rid of accept cookie button
    parent_element = driver.find_element(By.TAG_NAME, 'cms-cookie-disclaimer')
    shadow_root_element = driver.execute_script(
        'return arguments[0].shadowRoot', parent_element)
    accept_button = shadow_root_element.find_element(By.CLASS_NAME, 'accept-btn')
    accept_button.click()


    for k in kat:
        print(k)
        
        # step 1. -> import prices
        r = fake_headers(k[1], indProxy)
        prices_json = json.loads(r)

        prices_dict = {}
        for result_id, res in prices_json['results'].items():
            prices_dict[result_id] = res['price']

        driver.get(k[2])
        time.sleep(3)
        try:
            while driver.find_element(By.CLASS_NAME, 'mfcss_load-more-articles'):
                time.sleep(2)
                driver.find_element(By.CLASS_NAME, 'mfcss_load-more-articles').click()
        except Exception as e:
            print(e)
            pass

        for d in driver.find_elements(By.CLASS_NAME, 'title'):
            product = []
            product.append(web_site)
            product.append(store)
            product.append(date_str)
            product.append(d.get_attribute('href'))
            product.append(k[0])
            product.append(d.get_attribute('href').split('/')[5])
            product.append(d.get_attribute('description'))
            dict_key = f'{d.get_attribute("href").split("/")[5]}{d.get_attribute("href").split("/")[6]}'  # noqa: E501
            product.append(float(prices_dict[dict_key]))
            product.append(barcode)
            result.append(product)
        time.sleep(1)
    
    driver.quit()
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()