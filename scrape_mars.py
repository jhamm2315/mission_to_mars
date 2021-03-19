import requests
import pandas as pd
import json
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup as bs
import time

def scrape():
    #part 1
    executable_path = {'executable_path': r"C:\Users\jh231\Downloads\chromedriver_win32 (2)\chromedriver.exe"}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find_all('div',class_='list_text')
    for result in results:
    
        if result.find('a'):
            try:
                news_title = result.find('a').text
                news_p = result.find('div',class_='article_teaser_body').text
            except:
                pass

    #part 2
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    time.sleep(10)
    html2 = browser.html
    soup2 = bs(html2, 'lxml')
    results2 = soup2.find_all('div',class_='carousel_items')
    for result in results2:
        image_url = result.find('article')['style'].strip('background-image: url();')
        full_url = f"https://www.jpl.nasa.gov{image_url}"
        featured_image_url = full_url.replace("'",'')

    #part 3
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)
    time.sleep(5)
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ['Fact','Stat']
    mars_table = df.to_html()

    #part 4
    url_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced','https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    hemisphere_image_urls = []
    for url in url_list:
        browser.visit(url)
        html = browser.html
        time.sleep(5)
        soup = bs(html,'lxml')
        results = soup.find_all('div',class_='downloads')
        for result in results:
            if result.find('a')['href']:
                    img_url = result.find('a')['href']
        title = soup.find('h2',class_='title').text
        hemisphere_image_urls.append({'img_url':img_url,'title':title})

    mars_dictionary = {
        "headline":news_title,
        "article":news_p,
        "image_url":featured_image_url,
        "mars_tweet":mars_weather,
        "mars_table":mars_table,
        "hemisphere_urls":hemisphere_image_urls
    }

    browser.quit()

    return mars_dictionary
    
