import requests
from bs4 import BeautifulSoup

from selenium import webdriver
import time

import pandas as pd
import numpy as np

#page = requests.get('https://www.carthrottle.com/search/huracan/')
page = requests.get('https://www.carthrottle.com/topics/news/')

soup = BeautifulSoup(page.content, 'html.parser')
weblinks = soup.find_all("a", {"class": "headline"})

pagelinks = []
for link in weblinks[:100]:
	pagelinks.append('https://www.carthrottle.com'+link.get('href'))

title = []
thearticle = []
for link in pagelinks: 
	paragraphtext = []
	# get url
	url = link
	# get page text
	page = requests.get(url)
	# parse with BFS
	soup = BeautifulSoup(page.text, 'html.parser')
	atitle_container = soup.find(class_="headline-container")
	#print(atitle_container)
	atitle = atitle_container.find('h1')
	thetitle = atitle.get_text()
	article_container = soup.find(class_="content_field")
	article_p = article_container.find_all('p')
	#print(article_p[0].get_text())
	for paragraph in article_p:
		text = paragraph.get_text()
		paragraphtext.append(text)
	s = ''
	full_article = s.join(paragraphtext)
	#print(full_article)
	#print(thetitle)
	title.append(thetitle)
	thearticle.append(full_article)

data = {'Title':title, 'Article':thearticle, 'PageLink':pagelinks}
oldnews = pd.read_excel('news.xlsx')
news = pd.DataFrame(data=data)
cols = ['Title', 'Article', 'PageLink']
news = news[cols]

afronews = oldnews.append(news)
afronews.drop_duplicates(subset='Title', keep='last', inplace=True)
afronews.reset_index(inplace=True)
afronews.drop(labels='index', axis=1, inplace=True)

filename = 'news.xlsx'
wks_name = 'Data'

writer = pd.ExcelWriter(filename)
afronews.to_excel(writer, wks_name, index=False)

writer.save()