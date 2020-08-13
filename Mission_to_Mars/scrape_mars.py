from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import datetime as dt
import time
import re

def scrape():

	scrapedict = {}

	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', **executable_path, headless=False)

	url = "https://mars.nasa.gov/news/"
	browser.visit(url)

	time.sleep(1)

	html_string = browser.html

	soup = bs(html_string, 'html.parser')

	title = soup.find("div", class_="list_text").find("div", class_="content_title").text

	art_para = soup.find("div", class_="list_text").find("div", class_="article_teaser_body").text


	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)
	time.sleep(1)

	browser.find_by_id('full_image').click()

	browser.links.find_by_partial_text('more info').click()

	html_string = browser.html

	soup = bs(html_string, 'html.parser')

	image = soup.find("img", class_="main_image")['src']

	imagebase = "https://www.jpl.nasa.gov"

	featured_image_url = imagebase + image

	url = 'https://space-facts.com/mars/'

	tables = pd.read_html(url)

	df = tables[0]

	html_table = df.to_html()


	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url)
	time.sleep(1)

	aelement = browser.find_by_css('a.product-item h3')[0]

	firsttext = aelement.text

	aelement.click()

	firsturl = browser.links.find_by_text('Sample')[0]['href']

	browser.back()

	aelement = browser.find_by_css('a.product-item h3')[1]

	secondtext = aelement.text

	aelement.click()

	secondurl = browser.links.find_by_text('Sample')[0]['href']

	browser.back()

	aelement = browser.find_by_css('a.product-item h3')[2]

	thirdtext = aelement.text

	aelement.click()

	thirdurl = browser.links.find_by_text('Sample')[0]['href']

	browser.back()

	aelement = browser.find_by_css('a.product-item h3')[3]

	fourthtext = aelement.text

	aelement.click()

	fourthurl = browser.links.find_by_text('Sample')[0]['href']

	hemisphere_image_urls = [
	    {"title": firsttext, "img_url": firsturl},
	    {"title": secondtext, "img_url": secondurl},
	    {"title": thirdtext, "img_url": thirdurl},
	    {"title": fourthtext, "img_url": fourthurl},
	]

	scrapedict = {
		"Headline": title, 
		"Paragraph": art_para, 
		"Featured_image_url": featured_image_url, 
		"html_table": html_table,
		"hemisphere_info": hemisphere_image_urls
		}

	browser.quit()	

	return(scrapedict)
