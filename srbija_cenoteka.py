import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql


CATEGORIES = [
    ['Kandit','https://cenoteka.rs/proizvodi/slatkisi-i-grickalice/cokolade'],
    ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/deterdzent-za-posude'],
    ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/omeksivac-za-ves'],
    ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/praskasti-deterdzenti-za-ves']
]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    start_time = time.time()
    products = []
    unique_codes = set()

    for category in CATEGORIES:
        print(category)
        category_name, url = category
        
        web_page = fake_headers(url, 0)
        soup = BeautifulSoup(web_page, "html.parser")

        br_str = int(soup.find('ul', {'class':'pagination justify-content-center'})
                     .find_all('li')[-2].find('a').get_text())

        for x in range (1, br_str + 1):
            web_page = fake_headers(f'{url}?page={str(x)}', 0)
            soup = BeautifulSoup(web_page, "html.parser")

            for d in soup.find('div', {'id' : 'products'}).find_all('div'):
                if d.has_attr('data-product-id'):
                    # PL can be in multiple rows
                    # Scraping through rows
                    if d.find_all('div')[1].find('a'):
                        product_url = f'https://cenoteka.rs{d.find_all("div")[1].find("a").get("href")}'
                        code = str(d.find_all('div')[1].find('a').get('href')).split('/')[2]
                        name = d.find_all('div')[1].get_text().strip()
                        price_str = d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})
                        
                        if code not in unique_codes:
                            #IDEA
                            product = [
                                3,      # website
                                3,      # store
                                str(date.today()),  # date
                                product_url,
                                category_name,
                                code,
                                name,
                                float(price_str[0].get_text().strip().replace('-','0').replace('.','').replace(',','.'))
                            ]
                            if product[7] > 0:    
                                unique_codes.add(code)
                                products.append(product)
                            
                            
                            #Maxi
                            product = [
                                3,      # website
                                4,      # store
                                str(date.today()),  # date
                                product_url,
                                category_name,
                                code,
                                name,
                                float(price_str[1].get_text().strip().replace('-','0').replace('.','').replace(',','.'))
                            ]
                            if product[7] > 0:    
                                unique_codes.add(code)
                                products.append(product)
                            


                            #Univerexport
                            product = [
                                3,      # website
                                5,      # store
                                str(date.today()),  # date
                                product_url,
                                category_name,
                                code,
                                name,
                                float(price_str[2].get_text().strip().replace('-','0').replace('.','').replace(',','.'))
                            ]
                            if product[7] > 0:    
                                unique_codes.add(code)
                                products.append(product)
                            


                            #Tempo
                            product = [
                                3,      # website
                                6,      # store
                                str(date.today()),  # date
                                product_url,
                                category_name,
                                code,
                                name,
                                float(price_str[3].get_text().strip().replace('-','0').replace('.','').replace(',','.'))
                            ]
                            if product[7] > 0:    
                                unique_codes.add(code)
                                products.append(product)
                            


                            #DIS Rakovica
                            product = [
                                3,      # website
                                7,      # store
                                str(date.today()),  # date
                                product_url,
                                category_name,
                                code,
                                name,
                                float(price_str[4].get_text().strip().replace('-','0').replace('.','').replace(',','.'))
                            ]
                            if product[7] > 0:    
                                unique_codes.add(code)
                                products.append(product)
                            


                            #Roda
                            product = [
                                3,      # website
                                8,      # store
                                str(date.today()),  # date
                                product_url,
                                category_name,
                                code,
                                name,
                                float(price_str[5].get_text().strip().replace('-','0').replace('.','').replace(',','.'))
                            ]
                            if product[7] > 0:    
                                unique_codes.add(code)
                                products.append(product)
                            


                            
                            #Lidl - ubacujem provjeru je li postoji zadnji stupac - trgovina Lidl
                            if len(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})) > 6:
                                product = [
                                    3,      # website
                                    9,      # store
                                    str(date.today()),  # date
                                    product_url,
                                    category_name,
                                    code,
                                    name,
                                    float(price_str[6].get_text().strip().replace('-','0').replace('.','').replace(',','.'))
                                ]
                            if product[7] > 0:    
                                unique_codes.add(code)
                                products.append(product)
                        

    # inserting data
    insert_sql(products)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()