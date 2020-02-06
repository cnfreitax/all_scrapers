"""
use of script to create the login method
use a fake account!
"""

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs

class Login:
    def __init__(self, email, password, idPage):
        self.browser = webdriver.Chrome('/home/ekoar/chromedriver')
        self.email = email
        self.password = password
        self.idPage = idPage

    def signup(self, url):
        self.browser.get(url)
        sleep(0.5)

        emailInput = self.browser.find_element_by_xpath('//input[@class = "_2hvTZ pexuQ zyHYP"]')
        passwordInput = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input')

        emailInput.send_keys(self.email)
        sleep(0.2)
        passwordInput.send_keys(self.password)
        button = self.browser.find_element_by_xpath('//button[@class = "sqdOP  L3NKy   y3zKF     "]').click()
        sleep(4)
        buttonpu = self.browser.find_element_by_xpath('//button[@class = "aOOlW   HoLwm "]').click()

    def searchPage(self):
        buttonFind = self.browser.find_element_by_xpath('//input[@class = "XTCLo x3qfX "]')

        buttonFind.send_keys(self.idPage)
        sleep(0.9)
        resultSearch = self.browser.find_element_by_xpath('//a[@class = "yCE8d  "]').click()

    def scraper(self):
        lista_links = []
        bsObj = bs(self.browser.page_source, 'html.parser')
        sleep(3)
        publicacoes = bsObj.find_all('div', {'class':'Nnq7C weEfm'})
        lista_links.append(publicacoes)
