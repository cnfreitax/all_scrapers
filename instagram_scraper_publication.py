import os
import csv
from time import sleep
from tqdm import tqdm
from selenium import webdriver
from bs4 import BeautifulSoup as bs

cols = ['user', 'comment', 'data_comment', 'like' ]

main_url        = 'https://instagram.com'
url_login       = 'accounts/login/?source=auth_switcher'
url_publication = 'p/B6qJ22AhrI8/'
target_login    = f'{main_url}/{url_login}'
target_profile  = f'{main_url}/{url_publication}'
email           = 'el.rafa.canise'
password        = 'brioso2@19'

list_users          = []
list_comments       = []
list_datas_comments = []
list_likes          = []

if not os.path.exists('bs_scrape_itg_csv'):
    os.mkdir('bs_scrape_itg_csv')

browser = webdriver.Chrome('/home/ekoar/chromedriver')

browser.get(f'{main_url}/{url_login}')
sleep(0.5)
emailInput = browser.find_element_by_xpath('//input[@class = "_2hvTZ pexuQ zyHYP"]')
passwordInput = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')

emailInput.send_keys(email)
passwordInput.send_keys(password)

button = browser.find_element_by_xpath('//button[@class = "sqdOP  L3NKy   y3zKF     "]').click()

sleep(4)
buttonpu = browser.find_element_by_xpath('//button[@class = "aOOlW   HoLwm "]').click()

browser.get(f'{target_profile}')

sleep(0.5)
contador = 0
while(contador <= 20): #2650
    botaoMoreComment = browser.find_element_by_xpath('//button[@class = "dCJp8 afkep"]').click()
    contador += 1
    sleep(2)

with open(f'instagram_itau.csv', 'a') as file:
    dw = csv.DictWriter(file, fieldnames=cols, lineterminator='\n')
    dw.writeheader()
    users = browser.find_elements_by_xpath('//h3[@class = "_6lAjh "]')
    for user in users:
        user = user.text
        list_users.append(user)
        dw.writerow({
                        'user': user
                    })

    comments = browser.find_elements_by_tag_name('span')
    for comment in comments:
        comment = comment.text
        list_comments.append(comment)
        dw.writerow({
                        'comment': comment
                    })

    data_comments = browser.find_elements_by_xpath('//time[@class = "FH9sR Nzb55"]')
    for data_comment in data_comments:
        data_comment = data_comment.get_attribute('datetime')
        list_datas_comments.append(data_comment)
        dw.writerow({
                        'data_comment': data_comment
                    })

    likes = browser.find_elements_by_xpath('//button[@class = "FH9sR"]')
    for like in likes:
        like = like.text
        list_likes.append(like)
        dw.writerow({
                        'like': like
                    })
browser.quit()
