from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import urllib.request
from selenium import webdriver
import pandas as pd
import time

veggie_url = [
    'https://www.tokopedia.com/hot/makanan-vegetarian',
    'https://www.tokopedia.com/p/makanan-minuman/makanan-manis/buah-buahan',
    'https://www.tokopedia.com/hot/sayuran-segar', 
    'https://www.tokopedia.com/p/makanan-minuman/makanan-beku/buah'
    ]

# Headless browser configuration
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver/')
window_setting = 'window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;'

pageUrl = []
xpath_vegan_item_array = []
xpath_vegan_link_array = []
vegan_item_webEl_array = []
vegan_link_webEl_array = []
data = []

# 1
xpathVeganItemPromoLeft = '//*[@id="promo"]/div[2]/div[' 
xpathVeganItemPromoRight = ']/div/a[1]/div[2]/span'
xpathVeganLinkPromoLeft = '//*[@id="promo"]/div[2]/div['
xpathVeganLinkPromoRight = ']/div/a[2]'

#2
xpathItemPromoChildLeft = '//*[@id="promo-child-1"]/div[2]/div[' 
xpathItemPromoChildRight = ']/div/a[1]/div[2]/span'
xpathLinkPromoChildLeft = '//*[@id="promo-child-1"]/div[2]/div['
xpathLinkPromoChildRight = ']/div/a[2]'

#3
xpathItemSearchLeft = '//*[@id="search-result"]/div[2]/div/div/div[2]/div/div['
xpathItemSearchRight = ']/div/a/div[2]/h3'
xpathLinkSearchLeft = '//*[@id="search-result"]/div[2]/div/div/div[2]/div/div['
xpathLinkSearchRight = ']/div/a'

# get url
def getVeganPageUrl(baseUrl):
    for url in baseUrl:
        for countPage in range(1, 80):
            finalUrl = url + '?page=' + str(countPage)
            pageUrl.append(finalUrl)

# start scraping
def startScraping(url):
    driver.get(url)
    driver.execute_script(window_setting)

def getPath(item_left, item_right, link_left, link_right):
    for list in range(1,75):
        try:
            xpath_vegan_item = item_left + str(list) + item_right
            xpath_vegan_link = link_left + str(list) + link_right
            xpath_vegan_item_array.append(xpath_vegan_item)
            xpath_vegan_link_array.append(xpath_vegan_link)
        except(NoSuchElementException):
            pass

def getValueElement(xpath_item_array, xpath_link_array, page):
    vegan_item_array = []
    vegan_link_array = []
    print("Get value: " + page)
    for xpath in range(len(xpath_item_array)):
        try:
            item_xpath = driver.find_element_by_xpath(xpath_item_array[xpath])
            link_xpath = driver.find_element_by_xpath(xpath_link_array[xpath])
            vegan_item = item_xpath.text
            vegan_link = link_xpath.get_attribute("href")
            vegan_link = vegan_link.rsplit('/',2)[1]
            vegan_link = 'https://www.tokopedia.com/'+vegan_link
            vegan_item_array.append(vegan_item)
            vegan_link_array.append(vegan_link)
        except(NoSuchElementException):
            pass
    storeToArray(vegan_item_array, vegan_link_array, page)

def storeToArray(vegan_item_array, vegan_link_array, page):
    print("Store to array " + page + "\n")
    for item in range(len(vegan_item_array)):
        try:
            vegan_item = vegan_item_array[item]
            vegan_link = vegan_link_array[item]
            label = 'veg'
            row = {'item_name': vegan_item, 'shop_link':vegan_link, 'label': label, 'url':page}
            data.append(row)
        except(NoSuchElementException):
            pass

def saveToCsv(data_array):
    df = pd.DataFrame(data_array)
    df.to_csv('item_vegan.csv', index=False)

if __name__ == "__main__":
    #generate page url 1-62
    getVeganPageUrl(startUrl)
    #generate xpath
    getPath(xpathVeganItemPromoLeft, xpathVeganItemPromoRight,
            xpathVeganLinkPromoLeft, xpathVeganLinkPromoRight)
    getPath(xpathItemPromoChildLeft, xpathItemPromoChildRight,
            xpathLinkPromoChildLeft, xpathLinkPromoChildRight)
    getPath(xpathItemSearchLeft, xpathItemSearchRight,
            xpathLinkSearchLeft, xpathLinkSearchRight)
    # start scraping
    for url in pageUrl:
        try:
            print("Start scraping " + url)
            startScraping(url)
            getValueElement(xpath_vegan_item_array,
                            xpath_vegan_link_array, url)
        except(TimeoutException):
            print("TimeoutException! Sorry :( ")
            pass
    saveToCsv(data)
