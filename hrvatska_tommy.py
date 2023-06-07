import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql

kat =   [['Kandit', 'cokolade'],
        ['Kandit', 'bomboni-lizalice-zvakace-gume'],
        ['Kandit', 'bombonijere'],
        ['Kandit', 'bc1b9a2f-b7e2-4fac-b245-77da8fc09df5'],
        ['Kandit', 'sastojci'],
        ['Kandit', 'cokolade-i-bomboni'],
        ['Koestlin', 'stapici-pereci-krekeri-i-kokice'],
        ['Koestlin', 'keksi'],
        ['Saponia', 'tvrdi-sapuni'],
        ['Saponia', 'njega-zubi'],
        ['Saponia', 'sredstva-za-ciscenje'],
        ['Saponia', 'pranje-posuda'],
        ['Saponia', 'deterdzenti'],
        ['Saponia', 'omeksivaci-rublja-i-vode'],
        ['Saponia', 'odstranjivaci-mrlja-specijalna-sredstva'],
        ['Saponia', 'osvjezivaci-prostora'],
        ['Saponia', 'dezinfekcija-i-maske']]

url = 'https://spiza.tommy.hr/shop-api/taxon-products/by-code/keksi'

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result=[]
    indProxy = 0
    web_site = 19
    trgovina = 29
    date_str = str(date.today())
    start_time = time.time()
    for k in kat:
        print(k)
        headers = {
            "authority": "spiza.tommy.hr",
            "accept": "application/json, text/plain, */*",
            "accept-language": "hr-HR",
            "origin": "https://www.tommy.hr",
            "referer": "https://www.tommy.hr/",
            "sec-ch-ua": "^\^Not.A/Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^114^^, ^\^Google",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-tommy-client": "TommyWeb/1.0.0"
        }


        url = f'https://spiza.tommy.hr/shop-api/taxon-products/by-code/{k[1]}?limit=1000&page=1'
        r = fake_headers(url, indProxy, headers)
        data = json.loads(r)

        for d in data['items']:
            product=[]
            product.append(web_site)
            product.append(trgovina)
            product.append(date_str)
            product.append(f'https://www.tommy.hr/proizvodi/{d["slug"]}')
            product.append(k[0])
            product.append(d['code'])
            product.append(d['name'])
            code = d['code']
            product.append(float(d['variants'][code]['price']['current']/100))
            product.append(d['code'])
            result.append(product)
            
        time.sleep(1)

    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()        