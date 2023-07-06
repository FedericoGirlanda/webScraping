from typing import ItemsView
from pandas.core.frame import DataFrame
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import time
from tqdm import tqdm

chromedriver = ChromeDriverManager().install()
keywords = pd.read_csv('foods.csv', sep=",")

def search_google(search_query, totImages):
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--allow-cross-origin-auth-prompt')
    service = Service(executable_path=chromedriver)
    browser = webdriver.Chrome(service=service, options = options)

    # Open the browser to begin search
    browser.get(search_url) 
    accept_all = browser.find_element(By.XPATH, '//span[contains(text(),"Reject all")]')
    time.sleep(2)
    accept_all.click()
    time.sleep(1)

    for i in range(1,totImages+1):
        # Open the desired google images page browser to begin search
        browser.get(search_url)
        time.sleep(1)

        # XPath for the 1st image that appears in Google:
        img_box = browser.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img')
        # Click on the thumbnail
        img_box.click()
        time.sleep(1)

        # XPath of the image display 
        fir_img = browser.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')

        # Retrieve attribute of src from the element
        img_src = fir_img.get_attribute('src')

        search_query = search_query.replace(" ", "_")
        with open("img_src_links.csv", "a") as outfile:
                outfile.write(f"{search_query}|{img_src}\n")

    return img_src


# Creating header for file containing image source link 
with open("img_src_links.csv", "w") as outfile:
    outfile.write("search_terms|src_link\n")

# Loops through the list of search input
for keyword in tqdm(keywords['foods']):
    try:
        link = search_google(keyword, 20)
    except Exception as e: 
        print(e)