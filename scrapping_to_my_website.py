""" Web scrapping a mi sitio web, para obtener URL, Titulos y Bodys de los articulos. """

import requests
from bs4 import BeautifulSoup
from pprint import pprint

response = requests.get('https://nahuelbrandan.com/')
soup = BeautifulSoup(response.text, 'html.parser')
title = soup.title.text
print(title)

description = soup.select('meta[name=description]')[0]['content']
print(description)

articles = soup.find_all('div', {'class': 'thumbnail'})

for article in articles:
    print(article)
    print(article['a href'])
    print('asd')


articles_urls = [article['href'] for article in articles if 'href' in article]
pprint(articles_urls)
