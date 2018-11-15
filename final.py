from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time

startUrl = 'https://www.tokopedia.com/p/makanan-minuman/'

'''Headless browser configuration'''
options = Options()
options.headless = True
driver = webdriver.Chrome(
    options=options, executable_path='/usr/local/bin/chromedriver/')
window_setting = 'window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;'
# xpath only for promoted items
xpath_promoted_product_name = '//div[@id="promo-new"]//span[@class="detail__name"]'
xpath_promoted_link_shop = '//div[@id="promo-new"]//a[@class="muted"]'

data = []
xpath_item_array = []
xpath_link_array = []
xpath_list_product_content_dir = []
xpath_list_link_shop_content_dir = []
listWebElement_product = []
listWebElement_link = []
url = []

def getAllCategoryLink():
    print("Now getting all category link \n")
    a = driver.find_elements_by_xpath(
        '//div[@id="DeptIntermedController"]//div[@class="title ta-center"]//a')
    for i in range(len(a)):
        url.append(a[i].get_attribute("href"))

'''start the browser and get the web page'''
def getPage(urlpage):
    print("Now working on: " + str(urlpage))
    driver.get(urlpage)
    driver.execute_script(window_setting)
    time.sleep(30)

'''Get WebElement from xpath'''
def get_data_list(xpath_product_name, xpath_link_shop):
    try:
        result_link_shop = driver.find_elements_by_xpath(xpath_link_shop)
        result_product_name = driver.find_elements_by_xpath(xpath_product_name)
        store_data_to_array(result_product_name, result_link_shop)
    except(WebDriverException):
        for xpath in range(len(xpath_product_name)):
            result_link_shop = driver.find_elements_by_xpath(
                xpath_link_shop[xpath])
            result_product_name = driver.find_elements_by_xpath(
                xpath_product_name[xpath])
            listWebElement_product.append(result_product_name)
            listWebElement_link.append(result_link_shop)
            store_data_to_array(result_product_name, result_link_shop)

'''Get Xpath non promo'''
def get_list_data_content_dir():
    try:
        for index in range(1, 100):
            xpath_product_name = '//*[@id="content-directory"]/div[' + \
                str(index) + ']/div[2]/a[2]/div'
            xpath_link_shop = '//*[@id="content-directory"]/div[' + \
                str(index) + ']/div[3]/div/div[1]/div/div/div/a'
            xpath_list_product_content_dir.append(xpath_product_name)
            xpath_list_link_shop_content_dir.append(xpath_link_shop)
    except(NoSuchElementException):
        pass

'''Store data to array'''
def store_data_to_array(result_product_name, result_link_shop):
    try:
        for item_list in range(len(result_product_name)):
            item_name = result_product_name[item_list].text
            link_shop = result_link_shop[item_list].get_attribute("href")
            row = {"link_shop": link_shop, "item_name": item_name}
            data.append(row)
    except(AttributeError):
        pass

if __name__ == "__main__":    
    start_browser(urlpage)
    get_data_list(xpath_promoted_product_name, xpath_promoted_link_shop)
    get_list_data_content_dir()
    get_data_list(xpath_list_product_content_dir, xpath_list_link_shop_content_dir)
    store_data_to_array(listWebElement_product, listWebElement_link)

# save data to csv
# save data to db
