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
import socket

totImages = 100
chromedriver = ChromeDriverManager().install()
keywords = pd.read_csv('foods.csv', sep=",")

def scroll(driver):
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def search_google(search, nImages):
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search._2}"

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
    accept_all = browser.find_element(By.XPATH, '//span[contains(text(),"Accept all")]')
    time.sleep(2)
    accept_all.click()
    time.sleep(1)

    print("Category n "+str(search.Index+1)+"\n")
    for i in tqdm(range(1,nImages+1)):
        try:
            # Open the desired google images page browser to begin search
            browser.get(search_url)
            scroll(browser)
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

            #search.foods = search.foods.replace(" ", "_")
            with open("img_src_links.csv", "a") as outfile:
                    outfile.write(f"{search.foods}|{img_src}\n")
        except Exception as e: 
            pass

    return img_src


# Creating header for file containing image source link 
with open("img_src_links.csv", "w") as outfile:
    outfile.write("search_terms|src_link\n")

# List of categories and search labels
food_labels = pd.read_csv('foods.csv', sep=',')
socket.setdefaulttimeout(15)

# Loops through the list of search input
for keyword in food_labels.itertuples(index=True, name='Pandas'):
    try:
        link = search_google(keyword, totImages)
    except Exception as e: 
        print(e)