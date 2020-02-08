import os
import csv
import time
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

cols = ['users', 'comentarios',
        'data_comentarios', 'qtd_util'
]

main_url    = 'https://play.google.com/store/apps/details?id=br.com.'
url_profile = 'projetopolishop.mobile&hl=pt_BR&showAllReviews=true'
url_target  = f'{main_url}{url_profile}'

if not os.path.exists('database_gplay_polishop_csv'):
    os.mkdir('database_gplay_polishop_csv')

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
browser = webdriver.Chrome('/home/ekoar/chromedriver')

prefs = {
    'profile.default_content_setting_values.automatic_downloads': 1,
    'profile.managed_default_content_settings.images': 2
}

options.add_experimental_option('prefs', prefs)
with open(f'database_gplay_polishop.csv', 'a') as file:
    dw = csv.DictWriter(file, fieldnames=cols, lineterminator='\n')
    dw.writeheader()

    start = time.time()

    browser.get(url_target)
    page = browser.find_element_by_tag_name('html')
    contador = 0
    while(contador < 10):
        contador += 1
        page.send_keys(Keys.END)
        sleep(1)
        page.send_keys(Keys.HOME)
        sleep(1)
    users = []
    comentarios = []
    data_comentarios = []
    qtd_util = []

    for user in browser.find_elements_by_xpath('//span[@class = "X43Kjb"]'):
        user = user.text.strip()
        users.append(user)

    for comentario in browser.find_elements_by_xpath('//span[@jsname = "bN97Pc"]'):
        comentario = comentario.text.strip()
        comentarios.append(comentario)

    for data in browser.find_elements_by_xpath('//span[@class = "p2TkOb"]'):
        data = data.text.strip()
        data_comentarios.append(data)

    for like in browser.find_elements_by_xpath('//div[@class = "jUL89d y92BAb"]'):
        like = like.text.strip()
        qtd_util.append(like)

    for user in users:
        dw.writerow({
            'users': user
        })

    for comentario in comentarios:
        dw.writerow({
            'comentarios': comentario
        })

    for data in data_comentarios:
        dw.writerow({
            'data_comentarios': data
        })

    for like in qtd_util:
        dw.writerow({
            'qtd_util': like
        })

browser.quit()

end = time.time()
print(f'{len(comentarios)} comentários raspado em {end - start} segundos.')
