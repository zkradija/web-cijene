import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
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
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')

    result=[]
    indProxy = 0
    web_site = 4
    store = 3
    date_str = str(date.today())
    start_time = time.time()
    for k in kat:
        print(k)
        url = f'https://online.idea.rs/v2/categories/{k[2]}/products?per_page=1000&page=1&filter%5E%25%5E5Bsort%5E%25%5E5D=soldStatisticsDesc'
        r = fake_headers(url, indProxy)
        data = json.loads(r)
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
            result.append(product)
            
        time.sleep(1)
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()