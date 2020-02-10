import os
import csv
import time
from selenium import webdriver
from time import sleep
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

start = time.time()

cols = ['titulo', 'reclamacao', 'localizacao']

main_url = 'https://www.reclameaqui.com.br'
alvo = 'empresa/rappi_179520/lista-reclamacoes/?categoria=0000000000000311'
site_scp = f'{main_url}/{alvo}'
reclamacao_app = '&categoria=0000000000000311'

page = 3056

if not os.path.exists('scrape_rappi_csv'):
    os.makedirs('scrape_rappi_csv')

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
prefs = {
    'profile.default_content_setting_values.automatic_downloads': 1,
    'profile.managed_default_content_settings.images': 2
}

options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome('/home/ekoar/chromedriver')

lista_links = []

browser.get(site_scp)
bsObj = bs(browser.page_source, 'html.parser')

with open(f'raclame_aqui_rappi.csv', 'a') as file:
    dw = csv.DictWriter(file, fieldnames=cols, lineterminator='\n')
    dw.writeheader()
    for i in tqdm(range(page)):
        i = str(i + 1)
        browser.get(f'https://www.reclameaqui.com.br/empresa/rappi_179520/lista-reclamacoes/?pagina={i}{reclamacao_app}')
        bsObj = bs(browser.page_source, 'html.parser')
        sleep(2)
        boxes = bsObj.find_all('a', {'link-complain-id-complains'})
        lista_links = [box.get('href') for box in boxes]
        page_links = [f'{main_url}{link}' for link in lista_links]
        sleep(0.5)
        for link in page_links:
            browser.get(link)
            sleep(1.5)
            bs_page = bs(browser.page_source, 'html.parser')
            titulo = bs_page.find('h1', {'class':'ng-binding'}).text.strip()
            reclamacao = bs_page.find('div', {'class':'complain-body'}).find('p').text.strip()
            localizacao = bs_page.find('li', {'class':'ng-binding'}).text.strip()

            dw.writerow({
                            'titulo': titulo, 'reclamacao': reclamacao,
                            'localizacao': localizacao
                        })

end = time.time()
browser.quit()

print(f'Page crawleada em {end - start} segundos.' )
