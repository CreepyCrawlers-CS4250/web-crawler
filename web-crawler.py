import requests
from bs4 import BeautifulSoup
import csv

all_links = []

def add_to_report(link, num_outlinks):
    try:
        with open('report.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([link, num_outlinks])
    except:
        pass   

# def add_to_repository(title, header, link):
#     # do we make it .txt or .html???
#     try:
#         file_name = title + ';' + header + ';' + link + '.html'
#         f = open(file_name, "x")
#     except:
#         print("error. file already exists")
#         pass

def get_outlinks(links):
    outlinks = []
    for link in links:
            if 'href' in link.attrs:
                if link['href'] not in outlinks:
                    outlinks.append(link['href'])
    return outlinks

def creepy_crawler(link):
    # GET request on seed
    req = requests.get(link)


    # Get the link as BeautifulSoup object
    soup = BeautifulSoup(req.text, "html.parser")

    # Create a new file and save in repository folder
    # add_to_repository(soup.title.text, soup.h1.text, link)

    # Get all links for seed
    outlinks = get_outlinks(soup('a'))
    all_links.extend([outlink for outlink in outlinks if outlink not in all_links])
    # Add seed to report.csv
    add_to_report(link, len(outlinks))

seed = "https://en.wikipedia.org"
creepy_crawler(seed)

# print(soup.prettify())