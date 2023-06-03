import time
from datetime import date

import requests
from insert_sql import insert_sql


kat =   [['Kandit','https://online.idea.rs/#!/categories/60014036/mlecna-cokolada','60014036'],
        ['Kandit','https://online.idea.rs/#!/categories/60014037/cokolada-za-kuvanje','60014037'],
        ['Kandit','https://online.idea.rs/#!/categories/60014026/bombonjera','60014026'],
        ['Kandit','https://online.idea.rs/#!/categories/60014056/barovi','60014056'],
        ['Kandit','https://online.idea.rs/#!/categories/60014028/bombone-i-zvake','60014028'],
        ['Saponia','https://online.idea.rs/#!/categories/60016209/praskasti-deterdzent','60016209'],
        ['Saponia','https://online.idea.rs/#!/categories/60016210/tecni-deterdzent','60016210'],
        ['Saponia','https://online.idea.rs/#!/categories/60016211/kapsule','60016211'],
        ['Saponia','https://online.idea.rs/#!/categories/60007776/omeksivaci-i-oplemenjivaci-vesa','60007776'],
        ['Saponia','https://online.idea.rs/#!/categories/60016205/rucno-pranje','60016205'],
        ['Saponia','https://online.idea.rs/#!/categories/60016218/za-ciscenje-kuhinje','60016218'],
        ['Saponia','https://online.idea.rs/#!/categories/60016219/za-ciscenje-kupatila','60016219'],
        ['Saponia','https://online.idea.rs/#!/categories/60016220/za-ciscenje-podova-namestaja-stakla','60016220'],
        ['Saponia','https://online.idea.rs/#!/categories/60016221/za-dezinfekciju-eco-i-univerzalna','60016221'],
        ['Saponia','https://online.idea.rs/#!/categories/60007873/paste','60007873']]



def main():
    # identificiram se kao Chrome browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    result=[]
    web_site=4
    store = 3
    date_str = str(date.today())

    start_time = time.time()
    s = requests.Session()
    for k in kat:
        url = "https://online.idea.rs/v2/categories/" + str(k[2]) + "/products"
        querystring = {"per_page":"1000","page":"1","filter^%^5Bsort^%^5D":"soldStatisticsDesc"}
        r = s.request('GET', url, headers=headers, params=querystring)
        data = r.json()
        for d in data['products']:
            product = []
            product.append(web_site)
            product.append(store)
            product.append(date_str)
            product.append('https://online.idea.rs/#!' + d['product_path'])
            product.append(k[0])
            product.append(d['id'])
            product.append(d['name'])
            product.append(float(float(d['price']['amount']/100)))
            product.append(d['barcodes'][0][:13])
            result.append(product)
            print(product)
        time.sleep(1)
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()