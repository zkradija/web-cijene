import json
import time
from datetime import date, datetime

from headers import headers
from insert_sql import insert_sql


kat =   [['Kandit','Čokoladni proizvodi','0701'],
        ['Saponia', 'Sredstva za čišćenje i osveživači', '1305'],
        ['Saponia', 'Ručno pranje sudova', '130101'],
        ['Saponia', 'Deterdženti za veš i omekšivači', '1303'],
        ['Saponia', 'Paste za zube', '140101']]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result=[]
    indProxy = 0
    web_site = 5
    trgovina = 4
    date_str = str(date.today())

    # there is no barcode so im using dummy data
    barcode = ''    
    start_time = time.time()
    for k in kat:
        print(k)
        print(k[1])
        url_page_number = 'https://www.maxi.rs/api/v1/?operationName=GetCategoryProductSearch&variables=%7B%22lang%22%3A%22sr%22%2C%22searchQuery%22%3A%22%3Arelevance%22%2C%22sort%22%3A%22relevance%22%2C%22category%22%3A%22'+ str(k[2]) +'%22%2C%22pageNumber%22%3A0%2C%22pageSize%22%3A20%2C%22filterFlag%22%3Atrue%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2265b0b1aacb2caeea6468873e8f7fde0ef82ffb0c4f9c93583c41070fa1f13c82%22%7D%7D'
        r = headers(url_page_number, indProxy)
        data = json.loads(r)
        page_number = int(data['data']['categoryProductSearch']['pagination']['totalPages'])

        for x in range (0,page_number):
            url = 'https://www.maxi.rs/api/v1/?operationName=GetCategoryProductSearch&variables=%7B%22lang%22%3A%22sr%22%2C%22searchQuery%22%3A%22%3Arelevance%22%2C%22sort%22%3A%22relevance%22%2C%22category%22%3A%22' + str(k[2]) + '%22%2C%22pageNumber%22%3A' + str(x) + "%2C%22pageSize%22%3A20%2C%22filterFlag%22%3Atrue%2C%22plainChildCategories%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2265b0b1aacb2caeea6468873e8f7fde0ef82ffb0c4f9c93583c41070fa1f13c82%22%7D%7D"
            r = headers(url, indProxy)
            data = json.loads(r)

            for d in data['data']['categoryProductSearch']['products']:
                product=[]
                product.append(web_site)
                product.append(trgovina)
                product.append(date_str)
                product.append('https://maxi.rs' + d['url'])
                product.append(k[0])
                product.append(d['code'])
                product.append(d['name'])
                product.append(float(d['price']['unitPrice']))
                product.append(barcode)
                result.append(product)
                
            time.sleep(1)
    
    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()