""" Consultas HTTP a la web y analizar el contenido de su respuesta """

import requests
from bs4 import BeautifulSoup
from pprint import pprint

response = requests.get('https://platzi.com/')

print('Encoding of the website: %s' % response.encoding)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title.text)

response.encoding = 'utf-8'
print('Changed encoding to %s ' % response.encoding)

soup = BeautifulSoup(response.text, 'html.parser')

title = soup.title.text
print(title)

# ****

description = soup.select('meta[name=description]')[0]['content']
print(description)

categories_list = soup.find_all('div', {'class': 'HomeCategories-items'})[0]
categories = [category['href'] for category in categories_list]
pprint(categories)

# courses_links = soup.select('.Card-link')
# courses = [course['href'] for course in courses_links]
#
# print(courses)
