import requests
import lxml
from bs4 import BeautifulSoup
import re

#css-1oiyj28 new
#css-14fnihb old

url = 'https://www.olx.ro/d/piese-auto/'

aux_url = 'https://www.olx.ro'
f = requests.get(url)
soup = BeautifulSoup(f.content,'lxml')
links = soup.find_all('a',{'class':'css-1bbgabe'})
visited = []

# for link in links:
#     new_url = link['href']
#     if new_url[0] == '/':
#         new_url = aux_url + new_url;
#     print(new_url)
#     new_url_f = requests.get(new_url)
#     new_soup = BeautifulSoup(new_url_f.content, 'lxml')
#     if new_url[12] == 'o':
#         title = new_soup.find('h1').string
#     else:
#         title = new_soup.find('span', {'class': 'offer-title'}).getText().strip()
#
#     print(title)

visited.append(url)
toBeVisited = soup.find('ul',{'class':'pagination-list'}).find_all('a')
usedLinks = set()
toVisit = set()
for link in toBeVisited:
    toVisit.add(link['href'])

usedLinks.add('/d/piese-auto/')


def visitPages(currentPage):

    global usedLinks
    myUrl = url[:18]+currentPage
    f = requests.get(myUrl)
    newSoup = BeautifulSoup(f.content,'lxml')
    print(myUrl)

    getInfo(newSoup)

    toBeVisited = newSoup.find('ul',{'class':'pagination-list'}).find_all('a')
    newToVisit = set()
    for newPage in toBeVisited:
        newToVisit.add(newPage['href'])

    for nextPage in newToVisit:
        if nextPage not in usedLinks:
            usedLinks.add(nextPage)
            visitPages(nextPage)


def getInfo(newSoup):
    links = newSoup.find_all('a', {'class': 'css-1bbgabe'})
    for link in links:
        new_url = link['href']
        if new_url[0] == '/':
            new_url = aux_url + new_url
        print(new_url)
        new_url_f = requests.get(new_url)
        new_soup = BeautifulSoup(new_url_f.content, 'lxml')
        if new_url[12] == 'o':
            title = new_soup.find('h1').string
            description = new_soup.find('div',{'class':'css-g5mtbi-Text'}).getText()
            print(title,description,sep='\n')
        else:
            title = new_soup.find('span',{'class':'offer-title'}).getText().strip()
            details = new_soup.find('div',{'class':'offer-params'}).find_all('li',{'class':'offer-params__item'})
            print(title)
            for paramItem in details:
                label = paramItem.find('span').getText().strip()
                desc = paramItem.find('div').getText().strip()
                print(label,desc,sep=': ')

visitPages('/d/piese-auto/')



# f = requests.get('https://www.autovit.ro/anunt/jante-opel-adam-s-zafira-b-corsa-d-corsa-e-astra-h-meriva-b-noi-16-ID7GGRLw.html')
# new_soup = BeautifulSoup(f.content,'lxml')
# title = new_soup.find('span',{'class':'offer-title'}).getText().strip()
# details = new_soup.find('div',{'class':'offer-params'}).find_all('li',{'class':'offer-params__item'})
# for paramItem in details:
#     label = paramItem.find('span').getText().strip()
#     desc = paramItem.find('div').getText().strip()
#     print(label,desc,sep=': ')
# print(title)

#visitPages('/d/piese-auto/')

# add = True
# while add:
#     for nextPage in toVisit:
#         if nextPage

#
#     for link in links:
#         new_url = link['href']
#         if new_url[0] == '/':
#             new_url = aux_url + new_url;
#         print(new_url)
#         new_url_f = requests.get(new_url)
#         new_soup = BeautifulSoup(new_url_f.content, 'lxml')
#         if new_url[12] == 'o':
#             title = new_soup.find('h1').string
#         else:
#             title = new_soup.find('span',{'class':'offer-title'}).getText().strip()
#
#         print(title)

# for anchor in links:
#    print(anchor.string)

