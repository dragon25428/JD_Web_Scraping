from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from time import sleep
import pyodbc
pd.set_option('max_columns', 20, 'display.width', 120, 'max_colwidth', 120)

# Define search main page url
search_url = 'https://www.jd.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}

# Define get html soup function
def get_soup(input_url):
    response = requests.get(input_url, headers=headers)
    content = response.content
    soup_result = BeautifulSoup(content, 'lxml')
    return soup_result

# Define function to enter text for search
def search_product(browser, product='冰箱'):
    textbox = browser.find_element_by_xpath("//input[@id='key']")
    enter = browser.find_element_by_xpath("//button")
    textbox.clear()
    textbox.send_keys(product)
    enter.click()

# Define function to Flip Page
def next_page(browser):
    next_button = browser.find_element_by_css_selector('a.fp-next')
    if 'disabled' not in next_button.get_attribute('class'):
        next_button.click()

def last_page(browser):
    prev_button = browser.find_element_by_css_selector('a.fp-prev')
    if 'disabled' not in prev_button.get_attribute('class'):
        prev_button.click()

# Define function to scroll down the web page
def scroll_page(browser):
    scroll_max_time = 3
    last_height = browser.execute_script('return document.body.scrollHeight')
    while True:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(scroll_max_time)
        new_height = browser.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

# Run firefox web driver
driver = webdriver.Firefox()

# Get web page html
driver.get(search_url)

# Connect to SQL Server
connection = pyodbc.connect('DRIVER={SQL Server}; \
                       SERVER=10.188.34.5; \
                       DATABASE=Tmall_Data; \
                       UID=hsproot; \
                       PWD=Pl@ceholder1;')
cursor = connection.cursor()

# Start Crawling page by page
product_dict = {'item': [], 'price': [], 'comment': [], 'purchase_index': []}
search_product(driver)
while True:
    sleep(3)
    scroll_page(driver)  # scroll to page bottom
    items = driver.find_elements_by_css_selector('div.gl-i-wrap')  # retrieve all items on the page
    for item in items:
        item_name = item.find_element_by_class_name('p-name').find_element_by_tag_name('em').text  # item name
        price = item.find_element_by_css_selector('div.p-price').find_element_by_tag_name('i').text  # price
        comment_number = item.find_element_by_class_name('p-commit').find_element_by_tag_name('a').text  # comment number
        try:
            purchase_index = item.find_element_by_class_name('buy-score').find_element_by_tag_name('em').text  # purchase index (预购指数)
        except:
            purchase_index = '0'
        cursor.execute(u"INSERT INTO Product_List (item_name, price, comment_number, purchase_index) \
                        VALUES (N'{}', '{}', N'{}', '{}')".format(item_name, price, comment_number, purchase_index))
        connection.commit()
    next_button_js = driver.find_element_by_css_selector('a.fp-next')
    if 'disabled' not in next_button_js.get_attribute('class'):
        next_button_js.click()
    else:
        driver.close()  # close browser
        connection.close()  # close SQL connection
        break
