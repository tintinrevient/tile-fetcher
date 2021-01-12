import os
import shutil
import json
import csv
import re
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from time import time
import pyautogui
import pyperclip
import tile_fetcher


def csv_writer(data, outfile, append=False):
    mode = 'a' if append else 'w'
    with open(outfile, mode, encoding='utf-8') as csv_fh:
        csv_writer = csv.writer(csv_fh, delimiter=';')
        for row in data:
            csv_writer.writerow(row)


def csv_reader(infile):
    with open(infile, mode='r', encoding='utf-8') as csv_fh:
        csv_reader = csv.reader(csv_fh, delimiter=';')
        row_list = []
        for row in csv_reader:
            row_list.append(row)
    return row_list


def img_link_crawler(url, height, steps, outfile, append):

    data = []

    # initialize the driver
    chrome_options = Options()
    chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chrome_driver_binary = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(chrome_driver_binary, options=chrome_options)

    try:
        # open provided link in a browser window using the driver
        driver.get(url)

        # scroll down to the desired section
        driver.execute_script('window.scrollTo(0, ' + str(height) + ')')

        # find all the right arrows
        right_arrow_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.bYeTje.CMCEae.BcYSHe'))
        )

        sleep(1)

        # locate the image right arrow and click util the end of this image display section
        img_right_arrow = right_arrow_list[1]

        for _ in range(steps):
            ActionChains(driver).click(img_right_arrow).perform()
            sleep(1)

        # then all the image links will be loaded
        img_link_list = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.wcg9yf .vyQv6 a'))
        )

        # finally save all the image links
        for img_link in img_link_list:
            img_url = img_link.get_attribute('href')
            data.append([img_url])

    finally:
        # close the driver
        driver.close()

        # write the csv
        csv_writer(data, outfile, append=append)


    # close the driver
    driver.close()

    # write the csv
    csv_writer(data, outfile, append=append)


def img_link_crawler(infile, start_index, zoom):

    img_url_list = csv_reader(infile)

    for img_url in img_url_list[start_index:]:

        print('Image', img_url[0])

        tile_fetcher.main(img_url[0], zoom, False)


if __name__ == "__main__":

    data_dir_name = 'data'

    # Step 1 - Crawl all the image links
    #
    # url = 'https://artsandculture.google.com/entity/utrecht-caravaggism/m06rbhl'
    # height = 1100
    # steps = 8
    # append = False
    #
    # url = 'https://artsandculture.google.com/entity/caravaggisti/m0c3v8gh'
    # height = 1130
    # steps = 25
    # append = True
    #
    # img_link_crawler(url = url,
    #                  height = height,
    #                  steps = steps,
    #                  outfile = os.path.join(data_dir_name, 'images.csv'),
    #                  append = append)

    # Step 2 - Download all the images
    # start_index is added to resume the crawling after 'HTTP Error 429: Too Many Requests' issue
    img_link_crawler(infile = os.path.join(data_dir_name, 'images.csv'),
                     start_index = 229,
                     zoom = 2)
