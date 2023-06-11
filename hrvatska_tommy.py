import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit', 'cokolade'],
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
    ['Saponia', 'dezinfekcija-i-maske']
]

url = 'https://spiza.tommy.hr/shop-api/taxon-products/by-code/keksi'

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.time()
    products = []
    unique_codes = set ()

    for category in CATEGORIES:
        print(category)
        category_name, category_url = category
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


        url = f'https://spiza.tommy.hr/shop-api/taxon-products/by-code/{category_url}?limit=1000&page=1'
        response = fake_headers(url, 0, headers)
        data = json.loads(response)

        for product in data['items']:
            code = product['code']
            price = float(product['variants'][code]['price']['current']/100)
            if code not in unique_codes and price > 0:
                products.append([
                    19, # websiteA
                    29, # store
                    str(date.today()),  # date
                    f'https://www.tommy.hr/proizvodi/{product["slug"]}',  # product url
                    category_name,
                    code,
                    product['name'],
                    price
                ])
                unique_codes.add(code)
            
        time.sleep(1)

    # inserting data
    insert_sql(products)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()        