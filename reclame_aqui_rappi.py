import os
import csv
from selenium import webdriver
from bs4 import BeautifulSoup as bs

cols = ['titulo', 'comentario', 'local', 'data', 'respondido']

if not os.path.exists('scrape_rappi_csv'):
    os.makedirs('scrape_rappi_csv')

main_url = 'https://www.reclameaqui.com.br'
alvo = 'empresa/rappi_179520/lista-reclamacoes/'
site_scp = f'{main_url}/{alvo}' 


options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
prefs = {
    'profile.default_content_setting_values.automatic_downloads': 1,
    'profile.managed_default_content_settings.images': 2
}

options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome('chromedriver', options=options)

browser.get(site_scp)

bsObj = bs(browser.page_source, 'html.parser')

#listaObjs = bsObj.find('li', {'class':'ng-scope'}).find_all('a')
print(f'*************************')
listaObjs = bsObj.find('ul', {'class': 'complain-list'}).find_all('li')
print(listaObjs)

