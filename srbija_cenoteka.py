import time
from datetime import date, datetime

from bs4 import BeautifulSoup

from fake_headers import fake_headers
from insert_sql import insert_sql


kat =   [['Kandit','https://cenoteka.rs/proizvodi/slatkisi-i-grickalice/cokolade'],
         ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/deterdzent-za-posude'],
         ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/omeksivac-za-ves'],
         ['Saponia','https://cenoteka.rs/proizvodi/kucna-hemija/praskasti-deterdzenti-za-ves']]


def main():
    print(f'{__file__} : {datetime.now().strftime("%H:%M:%S")}')
    result = []
    indProxy = 0
    web_site = 3
    date_str = str(date.today())

    # there is no barcode so im using dummy data
    barcode = ''   
    start_time = time.time()
    for k in kat:
        print(k)
        web_page = fake_headers(k[1], indProxy)
        soup = BeautifulSoup(web_page, "html.parser")

        br_str = int(soup.find('ul', {'class':'pagination justify-content-center'})
                     .find_all('li')[-2].find('a').get_text())

        for x in range (1, br_str + 1):
            url = k[1] + '?page=' + str(x)
            web_page = fake_headers(url, indProxy)
            soup = BeautifulSoup(web_page, "html.parser")

            for d in soup.find('div', {'id' : 'products'}).find_all('div'):
                if d.has_attr('data-product-id'):
                    # PL can be in multiple rows
                    # Scraping through rows
                    if d.find_all('div')[1].find('a'):
                        #IDEA
                        product = []                
                        product.append(web_site)
                        product.append(3)
                        product.append(date_str)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1]
                                       .find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[0]
                                             .get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        product.append(barcode)
                        if product[7] != 0:    
                            result.append(product)
                        
                        
                        #Maxi
                        product = []
                        product.append(web_site)
                        product.append(4)
                        product.append(date_str)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1]
                                       .find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[1]
                                             .get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        product.append(barcode)
                        if product[7] != 0:    
                            result.append(product)
                        


                        #Univerexport
                        product = []
                        product.append(web_site)
                        product.append(5)
                        product.append(date_str)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1]
                                       .find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[2]
                                             .get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        product.append(barcode)
                        if product[7] != 0:    
                            result.append(product)
                        


                        #Tempo
                        product = []
                        product.append(web_site)
                        product.append(6)
                        product.append(date_str)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1]
                                       .find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[3]
                                             .get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        product.append(barcode)
                        if product[7] != 0:    
                            result.append(product)
                        


                        #DIS Rakovica
                        product = []
                        product.append(web_site)
                        product.append(7)
                        product.append(date_str)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1]
                                       .find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[4]
                                             .get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        product.append(barcode)
                        if product[7] != 0:    
                            result.append(product)
                        


                        #Roda
                        product = []
                        product.append(web_site)
                        product.append(8)
                        product.append(date_str)
                        product.append('https://cenoteka.rs' + d.find_all('div')[1]
                                       .find('a').get('href'))
                        product.append(k[0])
                        product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                        product.append(d.find_all('div')[1].get_text().strip())
                        product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[5]
                                             .get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                        product.append(barcode)
                        if product[7] != 0:    
                            result.append(product)
                        


                        
                        #Lidl - ubacujem provjeru je li postoji zadnji stupac - trgovina Lidl
                        if len(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})) > 6:
                            product = []
                            product.append(web_site)
                            product.append(9)
                            product.append(date_str)
                            product.append('https://cenoteka.rs' + d.find_all('div')[1]
                                           .find('a').get('href'))
                            product.append(k[0])
                            product.append(str(d.find_all('div')[1].find('a').get('href')).split('/')[2])
                            product.append(d.find_all('div')[1].get_text().strip())
                            product.append(float(d.find_all('div', {'class' : ['price', 'price p-0', 'price lowest p-0', 'price akcija star-top p-0']})[6]
                                                 .get_text().strip().replace('-','0').replace('.','').replace(',','.')))
                            product.append(barcode)
                        if product[7] != 0:    
                            result.append(product)
                        


    # inserting data
    insert_sql(result)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Elapsed time: {int(elapsed_time)} seconds')

if __name__ == "__main__":
    main()