import os
import csv
import time
from selenium import webdriver
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

start = time.time()

cols = [
        'titulo', 'reclamacao', 'localizacao',
         'status', 'classificador', 'data_reclamacao'
       ]

main_url  = 'https://www.reclameaqui.com.br'
alvo      = 'empresa/rappi_179520/lista-reclamacoes/?categoria=0000000000000311'
site_scp  = f'{main_url}/{alvo}'
categoria = '&categoria=0000000000000311'

page = 3074

if not os.path.exists('scrape_rappi_csv'):
    os.makedirs('scrape_rappi_csv')

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
prefs = {
    'profile.default_content_setting_values.automatic_downloads': 1,
    'profile.managed_default_content_settings.images': 2
}
options.add_experimental_option('prefs', prefs)

browser = webdriver.Chrome('/home/ekoar/chromedriver', chrome_options=options)

lista_links = []

browser.get(site_scp)
bsObj = bs(browser.page_source, 'html.parser')

with open(f'raclame_aqui_rappi.csv', 'a') as file:
    dw = csv.DictWriter(file, fieldnames=cols, lineterminator='\n')
    dw.writeheader()
    for i in tqdm(range(page)):
        i = str(i + 1)
        browser.get(f'https://www.reclameaqui.com.br/empresa/rappi_179520/lista-reclamacoes/?pagina={i}{categoria}')
        bsObj = bs(browser.page_source, 'html.parser')
        sleep(2)
        boxes = bsObj.find_all('a', {'link-complain-id-complains'})
        lista_links = [box.get('href') for box in boxes]
        page_links = [f'{main_url}{link}' for link in lista_links]
        sleep(0.5)
        for link in page_links:
            lista_palavras_chaves = []

            browser.get(link)
            sleep(0.3)
            bs_page = bs(browser.page_source, 'html.parser')
            sleep(2)
            titulo = bs_page.find('h1', {'class':'ng-binding'})
            titulo = titulo.text.strip()
            reclamacao = bs_page.find('div', {'class':'complain-body'}).find('p')
            reclamacao = reclamacao.text.strip()
            localizacao = bs_page.find('li', {'class':'ng-binding'}).text.strip()
            status = browser.find_element_by_xpath('//*[@id="complain-detail"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/span/img')
            status = status.get_attribute('title')
            palavras_chaves = bs_page.find_all('li', {'class':'ng-scope'})
            for classificador in palavras_chaves:
                classificador = classificador.text.strip()
                lista_palavras_chaves.append(classificador)
            classificador = str(lista_palavras_chaves).strip('[]').replace(',', ' -')
            data_reclamacao = browser.find_element_by_xpath('//li[@class = "ng-binding"][2]')
            data_reclamacao = data_reclamacao.text

            dw.writerow({
                            'titulo': titulo, 'reclamacao': reclamacao,
                            'localizacao': localizacao, 'status': status,
                            'classificador': classificador, 'data_reclamacao': data_reclamacao
                        })

            lista_palavras_chaves = []

end = time.time()
browser.quit()

print(f'Page crawleada em {end - start} segundos.' )
