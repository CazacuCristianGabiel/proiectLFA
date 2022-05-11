import string

import requests
from bs4 import BeautifulSoup

from category_model import categories
import re
import webbrowser, os

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
currentPage = 1
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
    global maxPageNumber
    myUrl = url[:18] + currentPage
    f = requests.get(myUrl)
    newSoup = BeautifulSoup(f.content, 'lxml')
    print("myUrl: ", myUrl)

    getInfo(newSoup)

    toBeVisited = newSoup.find('ul', {'class': 'pagination-list'}).find_all('a')
    newToVisit = set()
    for newPage in toBeVisited:
        newToVisit.add(newPage['href'])

    for nextPage in newToVisit:
        res = nextPage.split('page=')
        ind: str = (res[len(res) - 1])

        if ind.isnumeric():
            maxPageNumber = max(maxPageNumber, int(ind))
        if nextPage not in usedLinks:
            print(nextPage)
            usedLinks.add(nextPage)
            # visitPages(nextPage)


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
<br><br>

<h4>First page 1 </h4> 
<div style=" display: flex;
  flex-direction: row;">
<input type="button" id='script' name="scriptbutton" value=" Next Page " onclick="goPython()">

    <script src="http://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>

""".format(res=res)
html_template += """
<h4> Current Page: {currentPage}</h4> 
</div>
 """.format(currentPage=currentPage)
html_template += """
 <h4>Last page: {maxPageNumber} </h4> 
""".format(maxPageNumber=maxPageNumber)
ddd = """<script>
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
html_template += "<br><br></body></html>"

f.write(html_template)

f.close()

webbrowser.open(filePath)

print(maxPageNumber)

# pip install BeautifulSoup4
#
# (\d{3})[/\.\s](\d+)(\.|/|\s*[rR])(\d{2})[\W\.] pt anvelope dimensiuni
# (\d+),?.?(\d*)\s*([dD][eE]\s*)?([lL][eE][iI]+|[rR][oO][nN]|\/[bB][uU][cC]|[eE][uU][rR][Oo])+\s*\D preturi
# \W[vV][aA][rR][aAăĂ]+\W vara
# \W[iI][aA][rR][nN][aAăĂ]\W iarna
# \W[aA][lL]+[-\s][sS]?[eE][aA]?[sS][oO0][Nn]\W allseasons
# \W[mM][\s+][sS]\W m+s
#
# [pP][rR][oO][fF][iI][lL]([uU][lL])?\s*([dD][eE]\s*|[rR][aAăĂ][mM][aA][sS]\s*|[cC][cC][aA]\s*|\d*x\d*\-\s*|\-\s*|:\s*)(\d)([\.\-,]\d)?\s[mM]+
# profil
# multithreading- thread pull executer
#
# [A(\Wa)][uU][Dd][iI]+[^a-z] audi
#
# [M(\Wm)][eE][rR][CctTțȚ][eE][dD][eE][sSzZ][^a-z] mercedes
#
# [S(\Ws)][cCKk][oO][dD][aA]+[^a-z] skoda
#
# ([FVW]|([^a-z]|^)v|([^a-z]|^)w|([^a-z]|^)f)[oO0][lL]([țȚtTsS]+|[cCkK][sS])[vVwW][aA][gG][eEaAăĂÂâ][nN][^a-z] volkswagen
#
# [cC][oO][mM][pP][aA][tT][iI][bB][iI][lL][iI][tT][Aa][Tt][Ee]:?[ ]([A-Z]?[a-z])[\WA-Z] altele kind-of
#
# (N|([^a-z]|^)n)[oO][uUiIaAăĂ]+[^a-z] nou
#
# ((S|[^a-z]s)[eE][cC][oO][nN][dD][\s-,\.]*[hH][aAeE][nN][dD][^a-z]|(M|([^a-z]|^)m)[aAâÂîÎ][nN][aAăĂ]+([aA\s\-]+)?[dD][oO]([uU][aA]|[iI]+)) mana a doua

# si am avea filtre pentru latime anvelope, diametru anvelope, tipuri anvelope, preturi, profil anvelope, compatibilitate masini si conditie(nou/second hand)