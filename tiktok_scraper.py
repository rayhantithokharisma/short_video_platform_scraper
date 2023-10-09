#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dotenv import load_dotenv

"Load Selenium for pupeteering"
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service


import cv2 as cv
import numpy as np
import urllib.request

from selenium.webdriver.common.action_chains import ActionChains
from selenium_move_cursor.MouseActions import move_to_element_chrome


from fp.fp import FreeProxy


"Load Webdriver Installer"
from webdriver_manager.chrome import ChromeDriverManager

"Load Python Standard Modules"
import os, time, random, json, platform
from matplotlib import pyplot as plt
from collections import Counter

"Load BeautifulSoup Module"
from bs4 import BeautifulSoup

"Load Common Classes"


import requests
import json
import pandas as pd

from colorama import Fore, Back, Style
from colorama import init
from tqdm import tqdm
import sys
# pip install requests

init()

osID = platform.system().lower()

def configure():
    load_dotenv()

def load_driver():
    ### Using Selenium as a puppeteer for amazon scraper
    options = webdriver.ChromeOptions()    # options.add_argument("--headless")
    sec_ch_ua = '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"'
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    options.add_argument(f'--sec-ch-ua={sec_ch_ua}')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    ## When on mac load MAC DRIVER
    if 'darwin' in osID:
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    ## When on linux load LINUX DRIVER
    if 'linux' in osID:
        return webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
    ## When on linux load LINUX DRIVER
    if 'windows' in osID:
        service = Service(ChromeDriverManager(version='114.0.5735.90').install())
        return webdriver.Chrome(service = service, options=options)
        # return webdriver.Chrome(executable_path="D:\GEPHI\ARQUIVOSRLINUX\homeR\chromedriver.exe", options=options)

def solve_captcha(driver):
    while 1:
        try:    
            img = driver.find_element(By.ID,"captcha-verify-image")
            if img.get_attribute('src'):
                time.sleep(1)
                img.screenshot('foo_1.png')
                break
        except Exception as e:
            try:
                driver.find_element(By.XPATH,"//div[contains(text(), 'Authorize')]")
                return {'success':1}
            except Exception as e:
                raise e

    img = cv.imread('foo_1.png')
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray,15,0.05,1)
    corners = np.int0(corners)
    x_Array = []
    for i in corners:
        x,y = i.ravel()
        cv.circle(img,(x,y),3,255,-1)
        if x > 70:
            x_Array.append(x)

    x_Array.sort()
    slider = driver.find_element(By.CLASS_NAME,"captcha_verify_slide--slidebar")
    source = driver.find_element(By.CLASS_NAME,"secsdk-captcha-drag-icon")
    source_location = source.location
    source_size = source.size

    array = [170, 345, 400, 400, 345] 
    unic = Counter(x_Array) # проверка числа на уникальность, для устранения "гуляюших координат"
    for x in x_Array:
        if unic[x] > 1:
            x_offset = x-8
            break

    y_offset = 0
    action = ActionChains(driver)

    try:
        steps_count = 5
        step = (x_offset)/steps_count
        act_1 = action.click_and_hold(source)
        for x in range(0,steps_count):
            act_1.move_by_offset(step, y_offset)
        act_1.release().perform()

        msg = driver.find_element(By.CLASS_NAME,'msg').find_element(By.TAG_NAME,'div').text
        while msg == '':
            msg = driver.find_element(By.CLASS_NAME,'msg').find_element(By.TAG_NAME,'div').text
        print(msg)

        if 'Верификация пройдена' in msg or 'complete' in msg:
            return {'success':1}
        else:
            time.sleep(10)
            solve_captcha(driver)

    except Exception as e:
        print(e)

def main(driver,keyword):
    if '#' in keyword:
        # https://www.tiktok.com/tag/jairbolsonaro
        driver.get(f'https://www.tiktok.com/tag/{keyword.replace("#","")}')
        hashed = True
    else:
        ## Open page results with Keywork as query string
        driver.get(f'https://www.tiktok.com/search?q={keyword}')
        time.sleep(8)
        f=open("testing_tiktok_vm_12" + ".txt","w", encoding = 'utf-8')
        f.write(driver.page_source)
        f.close()
        msg = solve_captcha(driver)
        hashed = False



    delay = 10 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        print(f'{Fore.YELLOW}Page is ready!{Style.RESET_ALL}')
    except TimeoutException:
        print(f'{Fore.YELLOW}Page is ready!{Style.RESET_ALL}')


    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    n_pages = 15
    i = 0
    while i <= n_pages:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        i = i+1

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')


    if hashed:
        videoList = soup.find("div", {"data-e2e": "challenge-item-list"})
        allVids = videoList.findAll("div", {"class": "tiktok-x6y88p-DivItemContainerV2 e19c29qe7"})
    else:
        videoList = soup.find("div", {"mode": "search-video-list"})
        allVids = videoList.findAll("div", {"data-e2e": "search_top-item"})

    # allVids = videoList.findAll("div", {"class": "tiktok-1soki6-DivItemContainerForSearch e19c29qe9"})

    time.sleep(3)
    urls = [vid.find("a")['href'] for vid in allVids]
    print(f'\nFound total of {Fore.RED}{len(urls)}{Style.RESET_ALL} videos on this keyword.\n{Fore.GREEN}Start scraping{Style.RESET_ALL}')
    # print(f'\nFound total of {Fore.RED}{urls}{Style.RESET_ALL} videos on this keyword.\n{Fore.GREEN}Start scraping{Style.RESET_ALL}')
    music_urls_views = []
    music_urls = []
    stamp = time.time()
    urls = urls[:10]
    for idx, vid in enumerate(urls):
        sys.stdout.write("Scraped {}".format(idx))
        sys.stdout.flush()
        href = None
        driver.get(vid)
        time.sleep(1)
        vid_source = driver.page_source
        soup = BeautifulSoup(vid_source, 'html.parser')
        mus_con = soup.find("h4", {"data-e2e": "browse-music"})
        if mus_con is not None:
            href = mus_con.find('a', href = True)['href']
            if 'tiktok.com' not in href:
                vid_url = 'https://www.tiktok.com' + href
            else:
                vid_url = href
            if vid_url not in music_urls:
                driver.get(vid_url)
                time.sleep(1)
                mus_source = driver.page_source
                mus_soup = BeautifulSoup(mus_source, 'html.parser')
                mus = mus_soup.find("h2", {"data-e2e": "music-video-count"})
                if mus is not None:
                    mus_strong = mus.find("strong").get_text()
                    music_urls.append(vid_url)
                    music_urls_views.append(mus_strong)

    second_stamp = time.time()
    time_needed = second_stamp - stamp

    print('time_needed {}'.format(time_needed))
    df = pd.DataFrame()
    df['urls'] = music_urls
    df['num_vids'] = music_urls_views
    df.to_csv('tiktok_prd_{}.csv'.format('_'.join(keyword.split())), index = False)

if __name__ == '__main__':

    configure()
    if 'windows' in platform.system().lower():
        os.system('cls')
    else:
        os.system('clear')

    keywords = ['taylor swift enchanted']

    for keyword in keywords:
        driver = load_driver()
        time.sleep(2)
        json_object = main(driver,keyword)
    # driver.maximize_window()
    
    # login_btn = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@data-e2e='top-login-button']")))
    # login_btn.click()
    # user_login = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Use phone / email / username')]")))
    # user_login.click()
    # username = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Log in with email or username')]")))
    # username.click()
    # user = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@name='username']")))
    # user.send_keys('rayhantitho')
    # password = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@type='password']")))
    # password.send_keys('Titho__291298')
    # login = WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,".//*[@class='e1w6iovg0 tiktok-15aypwy-Button-StyledButton ehk74z00']")))
    # login.click()
    # print(f'  3. {Fore.RED}Start runing scraper setup - If asked, perform human authentication{Style.RESET_ALL}')
    # time.sleep(.5)

    # loged = False
    # while not loged:
    #     try:
    #         WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH,"//*[contains(text(), 'Login Successful')]")))
    #         loged = True
    #     except:
    #         loged = False

    
    # jsonFile = os.path.join('results', 'json', f'data_{keyword}.json')

    # jsonFile.write(json_object)
    # jsonFile.close()
