from bs4 import BeautifulSoup, SoupStrainer
import requests
import xlsxwriter
import time


# sa internet stranice https://Konzum.hr skinuti sve proizvode s pripadajućim cijenama (cca 6.100 proizvoda)
# cijene ću preuzeti sa stranice kategorija, gdje su navedeni proizvodi pojedine kategorije. ne treba otvarati stranicu pojedinačnog proizvoda

# identificiram se kao Firefox browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'Accept-Encoding': '*',
    'Connection': 'keep-alive'}

data=[]
kategorija = []

pocetak_vrijeme = time.time()
s = requests.Session()

response = s.get('https://www.konzum.hr/kreni-u-kupnju', headers=headers)
web_page = response.text
soup = BeautifulSoup(web_page, 'html.parser')

for a in soup.find_all('a', {'class': 'category-box__link'}):
    kat1 = []
    if str(a['href']).startswith('/web/'):
        kat1.append('https://konzum.hr' + a['href'])
        kat1.append(str(a.find('h3', {'class':'category-box__title'}).get_text()))
        kat1.append('1')
        kategorija.append(kat1)


#sada tražim kategorije po nivoima  - znam da ima max 3 lvla (nav-child-wrap-level-3)
#prvo idem nivo 2
for ul in soup.find_all('ul', {'class' : 'nav-child-wrap-level-2'}):
    kat2 = []
    kat2.append ('https://konzum.hr' + ul.a['href'])
    kat2.append (str(ul.a.get_text()).strip())
    kat2.append ('2')
    kategorija.append(kat2)

#a onda nivo 3    
for ul in soup.find_all('ul', {'class' : 'nav-child-wrap-level-3'}):
    for li in ul.find_all('li'):
        kat3 = []
        if li.a is not None:
            kat3.append ('https://konzum.hr' + li.a['href'])
            kat3.append (str(li.a.get_text()).strip())
            kat3.append('3')
            kategorija.append(kat3)

# sortiram - priprema za brisanje nadkategorija
kategorija.sort(key=lambda x: x[0])


#čistim kategorije od glavnih kategorija. zanimaju me samo najniži nivoi
i=0
br=len(kategorija)-1
while br>0:
    x = str(kategorija[i][0])
    x_kat=int(kategorija[i][2])
    y = str(kategorija[i+1][0])

    if y.startswith(x) and x_kat == 1: 
        del kategorija[i]
    else:
        i+=1
    br-=1


print('Kategorije pronađene: ' + time.strftime('%H:%M:%S') + ' h')

#brojac koristim radi izračuna brzine
counter=1
#krećem listanje proizvoda po kategorijama
t = time.localtime()

print('Proizvod broj ' + str(counter) + ' u ' + str(time.strftime("%H:%M:%S", t)))

for k in kategorija:
    response = s.get(k[0], headers=headers)
    web_page = response.text
    only_article_tags=SoupStrainer('article')   #i'm interested only in article tags
    soup = BeautifulSoup(web_page, 'html.parser', parse_only=only_article_tags)
    
    for article in soup.find_all('article'):
        product = []
        if article is not None: 
            product.append ('https://konzum.hr' + str(article.find('a', {'class' : 'link-to-product'})['href']))
            product.append (k[1])
            product.append (str(article.div.attrs['data-ga-id']))
            product.append (str(article.div.attrs['data-ga-name']))
            product.append (float(article.div.attrs['data-ga-price'].replace(" €","").replace(",",".")))    #prvo mičem oznaku €, zatim pretvaram decimalni zarez u točku, da bi na kraju pretvorio u broj
            data.append(product)
            counter+=1
            # counter to track the speed    
            if counter %500 == 0: 
                t = time.localtime()
                print('Proizvod broj ' + str(counter) + ' u ' + str(time.strftime("%H:%M:%S", t)))

#ubacujem nazive stupaca, radi prebacivanja u Excel
data.insert(0, ['poveznica','kategorija','sifra','naziv','cijena_EUR_kom'])

with xlsxwriter.Workbook('Konzum.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
    for row_num, data in enumerate(data):
        worksheet.write_row(row_num, 0, data)

kraj_vrijeme = time.time()
ukupno_vrijeme=kraj_vrijeme-pocetak_vrijeme
print(ukupno_vrijeme)
