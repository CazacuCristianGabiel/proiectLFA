import requests
import lxml
from bs4 import BeautifulSoup
# from mako.template import Template
from mako.template import Template
from category_model import categories
import re
# import module
import webbrowser, os

import subprocess

# in case chrome browser

# open html file

url = 'https://www.olx.ro/d/piese-auto/'

aux_url = 'https://www.olx.ro'
f = requests.get(url)
soup = BeautifulSoup(f.content, 'lxml')
links = soup.find_all('a', {'class': 'css-1bbgabe'})
visited = []
dataList = []
htmlFile = 'olx_piese.html'
filePath = 'file://' + os.path.realpath(htmlFile)
dataString = ""
maxPageNumber = 1
filterCount = 10
displayNonFound = True

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
toBeVisited = soup.find('ul', {'class': 'pagination-list'}).find_all('a')
usedLinks = set()
toVisit = set()
for link in toBeVisited:
    toVisit.add(link['href'])

usedLinks.add('/d/piese-auto/')


def visitPages(currentPage):
    global usedLinks
    myUrl = url[:18] + currentPage
    f = requests.get(myUrl)
    newSoup = BeautifulSoup(f.content, 'lxml')
    print("myUrl: ", myUrl)

    getInfo(newSoup)

    toBeVisited = newSoup.find('ul', {'class': 'pagination-list'}).find_all('a')
    newToVisit = set()
    for newPage in toBeVisited:
        newToVisit.add(newPage['href'])

    # for nextPage in newToVisit:
    #     if nextPage not in usedLinks:
    #         usedLinks.add(nextPage)
    #         visitPages(nextPage)


def isNullOrEmpty(str):
    return str is not None and str != "" and str != ''


def getInfo(newSoup):
    links = newSoup.find_all('a', {'class': 'css-1bbgabe'})
    global dataString
    counter = 0
    for link in links:
        if counter == 10:
            break
        counter += 1
        title = ''
        description = ''
        descriere = ''
        new_url = link['href']
        if new_url[0] == '/':
            new_url = aux_url + new_url
        print("new_url: ", new_url, ' ', counter)
        new_url_f = requests.get(new_url)
        # print("new_url: after ", new_url)Ï
        new_soup = BeautifulSoup(new_url_f.content, 'lxml')
        if new_url[12] == 'o':
            if new_soup.find('h1') is None: continue
            title = new_soup.find('h1').string
            description = new_soup.find('div', {'class': 'css-g5mtbi-Text'}).getText()

            # print("1 title: ", title, "description: ", description, sep='\n')
        else:
            if new_soup.find('span', {'class': 'offer-title'}) is not None:
                title = new_soup.find('span', {'class': 'offer-title'}).getText().strip()
                descriere = new_soup.find('div', {'class': 'offer-description__description'}).getText().strip()
                details = new_soup.find('div', {'class': 'offer-params'}).find_all('li',
                                                                                   {'class': 'offer-params__item'})
                # print("2 title: ", title, )
                for paramItem in details:
                    label = paramItem.find('span').getText().strip()
                    desc = paramItem.find('div').getText().strip()
                    description += (' ' + desc)
                    # print("3 label: ", label, "desc: ", desc, sep=': ')

        title = title.strip()
        if isNullOrEmpty(title):
            dataString += (' ' + title)
            dataList.append(title)

        description = description.strip()
        if isNullOrEmpty(description):
            dataString += (' ' + description)
            dataList.append(description)

        descriere = descriere.strip()
        if isNullOrEmpty(descriere):
            dataString += (' ' + descriere)
            dataList.append(descriere)
        # print("title: ", title, "description: ", description, "descriere: ", descriere, sep='\n %%% \n')


visitPages('/d/piese-auto/')

dataString = dataString.lower()


def findAllOccurrences():
    for category in categories:
        counter = 0
        for subCategory in category.subCategories.keys():
            if counter == filterCount:
                break
            counter += 1
            listOfOccurences = [_.start() for _ in re.finditer(subCategory, dataString)]
            # print('subCategory is ', subCategory, ', listOfOccurences: ', listOfOccurences)
            category.subCategories[subCategory] = len(listOfOccurences)


findAllOccurrences()


def data_to_html_table(categories: dict):
    html = ''
    for category in categories:
        html += '<h2>{title} </h2>'.format(title=category.title)
        html += '<table style="width:100% border:1px solid black;">'
        for name, value in category.subCategories.items():
            if not displayNonFound and value == 0:
                continue
            html += '<tr style="border:1px solid black;">'
            # for subCategory in category.subCategories.keys():
            html += '<td>'
            html += name
            html += '</td>'

            html += '<td>'
            html += str(value)
            html += '</td>'

            html += '</tr>'

        html += '</table>'
    return html


res = data_to_html_table(categories)

f = open(htmlFile, 'w')

headStyle = """
  <head><style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
    """
html_template = """<html>"""
html_template += headStyle
html_template += """<body>
{res}
<input type="button" id='script' name="next page" value=" Run Script " onclick="goPython()">

    <script src="http://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
 
""".format(res=res)
ddd = """    <script>
        function goPython(){
            $.ajax({
              url: "crawler.py",
             context: document.body
            }).done(function() {
             alert('finished python script');;
            });
        }
    </script>
    """
html_template += ddd
html_template += "</body></html>"

f.write(html_template)

f.close()

webbrowser.open(filePath)

# pip install BeautifulSoup4
