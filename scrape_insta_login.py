import os
import csv
from time import sleep
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from signup_instagram import Login


cols = ['user_name', 'comentario']

main_url  = 'https://instagram.com'
url_login = 'accounts/login/?source=auth_switcher'
profile   = 'polishop/'
target_login = f'{main_url}/{url_login}'
target_profile = f'{main_url}/{profile}'

if not os.path.exists('bs_scrape_itg_csv'):
    os.mkdir('bs_scrape_itg_csv')

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')

prefs = {
    'profile.default_content_setting_values.automatic_downloads': 1,
    'profile.managed_default_content_settings.images': 2
}

options.add_experimental_option('prefs', prefs)
with open(f'instagram_database.csv', 'a') as file:
    dw = csv.DictWriter(file, fieldnames=cols, lineterminator='\n')
    dw.writeheader()
    login = Login('el.rafa.canise', 'brioso2@19', 'polishop')
    login.signup('https://www.instagram.com/accounts/login/?source=auth_switcher')
    login.searchPage()
    sleep(2)
    login.scraper()
