# Dependencies
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

executable_path = {'executable_path': 'chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    finalData = {}
    output = marsNews()
    finalData["mars_news"] = output[0]
    finalData["mars_paragraph"] = output[1]
    finalData["mars_image"] = marsImage()
    finalData["mars_weather"] = marsWeather()
    finalData["mars_facts"] = marsFacts()
    finalData["mars_hemisphere"] = marsHem()
    return finalData


# NASA Mars News
def marsNews():
    news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='slide')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="rollover_description_inner").text
    output = [news_title, news_p]
    return output

# Mars Space Images 
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

# Mars Weather
def marsWeather():
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')
    
    # Scrape the tweet info and return
    first_tweet = tweet_soup.find('p', class_='TweetTextSize').text
    return first_tweet

# Mars Facts
def marsFacts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ['Property', 'Value']
    # Set index to property in preparation for import into MongoDB
    df.set_index('Property', inplace=True)
    
    # Convert to HTML table string and return
    return df.to_html()

# Mars Hemispheres
def marsHem():
    import time 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere
