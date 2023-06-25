import json
import requests
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql

CATEGORIES = [
    ['Kandit', 'Sladko in slano', 'Sladki prigrizki', 'Čokolade'],
    ['Kandit', 'Sladko in slano', 'Sladki prigrizki', 'Bonboni'],
    ['Kandit', 'Sladko in slano', 'Sladki prigrizki', 'Bonboniere'],
    ['Kandit', 'Sladko in slano', 'Sladki prigrizki', 'Čokoladne rezine'],
    ['Kandit', 'Sladko in slano', 'Sladki prigrizki', 'Čokoladne banane'],
    ['Saponia', 'Osebna nega', 'Nega ust in zob', 'Zobne paste'],
    ['Saponia', 'Osebna nega', 'Nega ust in zob', 'Zobne paste za otroke'],
    ['Saponia', 'Dom', 'Pranje perila', 'Mehčalci'],
    ['Saponia', 'Dom', 'Pranje perila', 'Tekoči pralni praški'],
    ['Saponia', 'Dom', 'Pranje perila', 'Pralni praški v kapsulah'],
    ['Saponia', 'Dom', 'Pranje perila', 'Trdi pralni praški'],
    ['Saponia', 'Dom', 'Detergetni za pomivanje posode', 'Strojno pomivanje posode'],
    ['Saponia', 'Dom', 'Detergetni za pomivanje posode', 'Ročno pomivanje posode'],
    ['Saponia', 'Dom', 'Čistila', 'Druga čistila'],
    ['Saponia', 'Dom', 'Čistila', 'Čistila za kuhinjo'],
    ['Saponia', 'Dom', 'Čistila', 'Univerzalna čistila'],
    ['Saponia', 'Dom', 'Čistila', 'Čistila za steklo']
]

web_category_name = 'Sladko in slano'
subcategory_name =  'Sladki prigrizki'
filter_pproperties_categories = 'Čokolade'


web_category_name = 'Dom'
filter_pproperties_categories = 'Mehalčci'
subcategory_name =  'Pranje perila'


def main():
    
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()

    for category in CATEGORIES:
        print(category)
        category_name, web_category_name, web_subcategory_name, web_filterProperties_categories = category

        cookies = {
            'storeID': '5861',
            '_hjFirstSeen': '1',
            '_hjIncludedInSessionSample_2790117': '0',
            '_hjSession_2790117': 'eyJpZCI6ImIxNGRmNzU2LTUyMmItNDViYS1iNDIxLWZkZTg5ZjhmMjViOCIsImNyZWF0ZWQiOjE2ODc3MTA4OTc5ODcsImluU2FtcGxlIjpmYWxzZX0=',
            '_hjAbsoluteSessionInProgress': '1',
            '_ga': 'GA1.1.887435997.1687710911',
            '_hjSessionUser_2790117': 'eyJpZCI6IjYxMjI3ZTY2LTM3MDgtNWZmZS1iMjUyLTJiNWY5NDU0NDgyOCIsImNyZWF0ZWQiOjE2ODc3MTA4OTc5NzgsImV4aXN0aW5nIjp0cnVlfQ==',
            '_ga_01FGFBLMLX': 'GS1.1.1687710911.1.0.1687711473.0.0.0',
        }

        headers = {
            'authority': 'hitrinakup.com',
            'accept': '*/*',
            'accept-language': 'hr,en-US;q=0.9,en;q=0.8,de;q=0.7,es;q=0.6,vi;q=0.5,zh-CN;q=0.4,zh;q=0.3,sr;q=0.2,sl;q=0.1,bs;q=0.1',
            'apiversion': '3.2',
            'content-type': 'application/json',
            # 'cookie': 'storeID=5861; _hjFirstSeen=1; _hjIncludedInSessionSample_2790117=0; _hjSession_2790117=eyJpZCI6ImIxNGRmNzU2LTUyMmItNDViYS1iNDIxLWZkZTg5ZjhmMjViOCIsImNyZWF0ZWQiOjE2ODc3MTA4OTc5ODcsImluU2FtcGxlIjpmYWxzZX0=; 
            # _hjAbsoluteSessionInProgress=1; _ga=GA1.1.887435997.1687710911; _hjSessionUser_2790117=eyJpZCI6IjYxMjI3ZTY2LTM3MDgtNWZmZS1iMjUyLTJiNWY5NDU0NDgyOCIsImNyZWF0ZWQiOjE2ODc3MTA4OTc5NzgsImV4aXN0aW5nIjp0cnVlfQ==; 
            # _ga_01FGFBLMLX=GS1.1.1687710911.1.0.1687711473.0.0.0',
            'origin': 'https://hitrinakup.com',
            'referer': 'https://hitrinakup.com/kategorije/Sladko%20in%20slano/Sladki%20prigrizki',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sessionid': 'b08dae1c-265c-4112-b4b3-2f19bf3ebc72',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        json_data = {
            'operationName': 'getItemsForSelectedSubCategory',
            'variables': {
                'storeId': '5861',
                'categoriesLimit': 1000,
                'categoriesSkip': 0,
                'subcategoryName': web_subcategory_name,
                'cypherQuery': '123a17d4-b159-4976-ac50-8590059b48c0',
                'filterProperties': {
                    'categories': [
                        web_filterProperties_categories,
                    ],
                },
                'categoryName': web_category_name,
                'date': 'Sun Jun 25 2023',
            },
            'query': 'query getItemsForSelectedSubCategory($storeId: String, $categoriesLimit: Int, $categoriesSkip: Int, $subcategoryName: String, $cypherQuery: String, '
                        '$filterProperties: FilterUpdateInput, $categoryName: String, $date: String) {\n  getItemsForSelectedSubCategory(\n    storeId: $storeId\n    categoriesLimit: $categoriesLimit\n'
                        'categoriesSkip: $categoriesSkip\n    subcategoryName: $subcategoryName\n    filterProperties: $filterProperties\n    cypherQuery: $cypherQuery\n    categoryName: $categoryName\n'
                        'date: $date\n  ) {\n    name\n    filters {\n      general {\n        name\n        itemCount\n        __typename\n      }\n      brands {\n        name\n        itemCount\n'
                        '__typename\n      }\n      categories {\n        name\n        itemCount\n        __typename\n      }\n      allergens {\n        name\n        itemCount\n        __typename\n      }'
                        '\n      __typename\n    }\n    items {\n      weighing\n      weight\n      itemId\n      EAN\n      name\n      orderLimit\n      price\n      discountedPrice\n      lowQuantity\n'
                        'promotionDisplayPrice\n      promotionType\n      promotionDisplayProcentage\n      promotionProcentage\n      alcohol\n      group\n      quantity\n      itemWeighingChangeQuantityStep\n'
                        'inStock\n      priceEm\n      em\n      badges\n      type\n      comment\n      discountEan\n      id\n      displayName\n      itemBackground\n      bannerColor\n      bannerTextBold\n'
                        'bannerTextNormal\n      bannerTextColor\n      img\n      favourite\n      brand\n      category\n      __typename\n    }\n    __typename\n  }\n}\n',
        }

        response = requests.post('https://hitrinakup.com/graphql', cookies=cookies, headers=headers, json=json_data)

        data = response.json()

        for product in data['data']['getItemsForSelectedSubCategory']['items']:
            code = product['id']
            price = float(product['price'])
            if code not in unique_codes and price > 0:      # Only add the product if its code is not already in the set
                products.append ([
                    9,  # website
                    19,  # store
                    str(date.today()),
                    f'https://hitrinakup.com/izdelki/{code}/{product["displayName"]}',
                    category_name,
                    code,  # code
                    product['name'],  # name
                    price  # price
                ])
                unique_codes.add(code)        
        time.sleep(1)

    # inserting data
    insert_sql(products)

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()