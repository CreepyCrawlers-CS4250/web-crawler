import requests
from bs4 import BeautifulSoup
import csv

all_links = []

def addToReport(link, outlinks):
    try:
        with open('report.csv', 'a') as csvfile:
            csvfile.writerow({link["href"]}, outlinks)
    except:
        pass   

def addToRepository(link):
    # do we make it .txt or .html???
    try:
        fileName = f'{soup.title.text}; {soup.h1.text}; {link["href"]}.html'
        f = open(fileName, "x")
    except:
        print("error. file already exists")
        pass

def getOutlinks(link):
    pages = []
    for link in soup("a"):
        if 'href' in link.attrs:
            print(link['href'])
            pages.append(link['href'])
    return pages

def creepy_crawler(link):
    # GET request on seed
    req = requests.get(link)


    # Get the link as BeautifulSoup object
    soup = BeautifulSoup(req.text, "html.parser")

    # Create a new file and save in repository folder
    addToRepository(link)

    # Get all links for seed
    outlinks = getOutlinks(link)
    all_links.extend(outlinks)
    # Add seed to report.csv
    addToReport(link, len(outlinks))

seed = "https://en.wikipedia.org/wiki/Main_Page"
creepy_crawler(seed)













# print(soup.prettify())

