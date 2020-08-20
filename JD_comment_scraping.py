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

# Run firefox web driver
driver = webdriver.Firefox()

# Get web page html
driver.get(search_url)

# Define function to enter text for search
def search_product(browser, product='冰箱'):
    textbox = browser.find_element_by_xpath("//input[@id='key']")
    enter = browser.find_element_by_xpath("//button")
    textbox.clear()
    textbox.send_keys(product)
    enter.click()





