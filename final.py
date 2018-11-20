from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import urllib.request
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

xpath_category = '//div[@id="DeptIntermedController"]//div[@class="title ta-center"]//a'
item_left_1 = '//*[@id="content-directory"]/div['
item_right_1 = ']/div[2]/a[2]/div'
link_left_1 = '//*[@id="content-directory"]/div['
link_right_1 = ']/div[3]/div/div[1]/div/div/div/a'
# xpath only for promoted items
xpath_promoted_item = '//div[@id="promo-new"]//span[@class="detail__name"]'
xpath_promoted_shop = '//div[@id="promo-new"]//a[@class="muted"]'

categoryUrl = []
pageUrl = []
data = []
xpath_item_array = []
xpath_link_array = []

def startScraping(url):
    driver.get(url)
    driver.execute_script(window_setting)

# get category
def getCategoryUrl(xpath):
    categoryElement = driver.find_elements_by_xpath(xpath)
    for element in range(len(categoryElement)):
        categoryUrl.append(categoryElement[element].get_attribute("href"))

#get page each category
def getPageUrl(category):
    for countPage in range(72, 91):
        for categoryUrl in category:
            categoryPage = categoryUrl + '?page=' + str(countPage)
            pageUrl.append(categoryPage)

def getPath(item_left, item_right, link_left, link_right):
    for list in range(1, 75):
        try:
            xpath_item = item_left + str(list) + item_right
            xpath_link = link_left + str(list) + link_right
            xpath_item_array.append(xpath_item)
            xpath_link_array.append(xpath_link)
        except(NoSuchElementException):
            pass

def getValueElement(xpath_item_array, xpath_link_array, page):
    item_array = []
    link_array = []
    print("Get value: " + page)
    for xpath in range(len(xpath_item_array)):
        try:
            item_xpath = driver.find_element_by_xpath(xpath_item_array[xpath])
            link_xpath = driver.find_element_by_xpath(xpath_link_array[xpath])
            item = item_xpath.text
            link = link_xpath.get_attribute("href")
            item_array.append(item)
            link_array.append(link)
        except(NoSuchElementException):
            pass
    storeToArray(item_array, link_array, url)

def storeToArray(item_name_array, shop_url_array, page):
    print("Store to array " + page + "\n")
    for item in range(len(item_name_array)):
        try:
            item_name = item_name_array[item]
            shop_url = shop_url_array[item]
            row = {'item_name': item_name, 'shop_link': shop_url, 'url': page}
            data.append(row)
        except(NoSuchElementException):
            pass

def saveToCsv(data_array):
    df = pd.DataFrame(data_array)
    df.to_csv('item_food.csv', index=False)

if __name__ == "__main__":
    #start page
    startScraping(startUrl)
    #get category link
    getCategoryUrl(xpath_category)
    #get page url. generate url setiap kategori dan setiap halaman
    getPageUrl(categoryUrl)
    #get path
    getPath(item_left_1, item_right_1, link_left_1, link_right_1)
    # start scraping
    for url in pageUrl:
        try:
            print("Start scraping " + url)
            startScraping(url)
            getValueElement(xpath_item_array, xpath_link_array, url)
            getValueElement(xpath_promoted_item, xpath_promoted_shop, url)
        except(TimeoutException):
            print("TimeoutException! Sorry :( ")
            pass
    saveToCsv(data)
