import json
import time
from datetime import date, datetime

from fake_headers import fake_headers
from insert_sql import insert_sql


CATEGORIES = [
    ['Kandit','Čokoladni proizvodi','0701'],
    ['Saponia', 'Sredstva za čišćenje i osveživači', '1305'],
    ['Saponia', 'Ručno pranje sudova', '130101'],
    ['Saponia', 'Deterdženti za veš i omekšivači', '1303'],
    ['Saponia', 'Paste za zube', '140101']
]

def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.perf_counter()
    products = []
    unique_codes = set()
    
    for category in CATEGORIES:
        print(category)
        category_name, category_name_2, category_code = category
        
        url_page_number = f'https://www.maxi.rs/api/v1/?operationName=GetCategoryProductSearch&variables=%7B%22lang%22%3A%22sr%22%2C%22searchQuery%22%3A%22%3Arelevance%22%2C%22sort%22%3A%22relevance%22%2C%22category%22%3A%22{category_code}%22%2C%22pageNumber%22%3A0%2C%22pageSize%22%3A20%2C%22filterFlag%22%3Atrue%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2265b0b1aacb2caeea6468873e8f7fde0ef82ffb0c4f9c93583c41070fa1f13c82%22%7D%7D'
        response = fake_headers(url_page_number, 0)
        data = json.loads(response)
        page_number = int(data['data']['categoryProductSearch']['pagination']['totalPages'])

        for x in range (0,page_number + 1):
            url = f'https://www.maxi.rs/api/v1/?operationName=GetCategoryProductSearch&variables=%7B%22lang%22%3A%22sr%22%2C%22searchQuery%22%3A%22%3Arelevance%22%2C%22sort%22%3A%22relevance%22%2C%22category%22%3A%22{category_code}%22%2C%22pageNumber%22%3A{x}%2C%22pageSize%22%3A20%2C%22filterFlag%22%3Atrue%2C%22plainChildCategories%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2265b0b1aacb2caeea6468873e8f7fde0ef82ffb0c4f9c93583c41070fa1f13c82%22%7D%7D'
            response = fake_headers(url, 0)
            data = json.loads(response)

            for product in data['data']['categoryProductSearch']['products']:
                code = product['code']
                price = float(product['price']['discountedPriceFormatted'].replace(' RSD','')
                              .replace('.','').replace(',','.'))
                if code not in unique_codes and price > 0:
                    products.append([
                        4,  # store
                        str(date.today()),
                        f'https://maxi.rs{product["url"]}',
                        category_name,
                        code,
                        product['name'],
                        price,
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