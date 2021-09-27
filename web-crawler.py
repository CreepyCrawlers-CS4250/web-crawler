import requests
from bs4 import BeautifulSoup
import csv

all_links = []
counter = 0

def add_to_report(link, num_outlinks):
    try:
        with open('report.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([link, num_outlinks])
    except:
        pass   

def add_to_repository(text):
    # do we make it .txt or .html???
    global counter
    file_name = 'repository/{}.html'.format(counter)
    f = open(file_name, "w", encoding="utf-8")
    f.write(text)
    counter += 1

def get_outlinks(links):
    outlinks = []
    for link in links:
            if 'href' in link.attrs:
                if 'https://' in link['href'] or 'http://' in link['href']:
                    if link['href'] not in outlinks:
                        outlinks.append(link['href'])
    return outlinks

def creepy_crawler(link):
    # print(link)
    # GET request on seed
    req = requests.get(link)


    # Get the link as BeautifulSoup object
    soup = BeautifulSoup(req.text, "html.parser")

    # Create a new file and save in repository folder
    add_to_repository(req.text)

    # Get all links for seed
    outlinks = get_outlinks(soup('a'))
    all_links.extend([outlink for outlink in outlinks if outlink not in all_links])
    #print(all_links)
    # Add seed to report.csv
    add_to_report(link, len(outlinks))

    global counter
    if counter > 500:
        return "done"
    else:
        creepy_crawler(all_links.pop(0))

seed = "https://en.wikipedia.org"
# all_links.append(seed)
creepy_crawler(seed)

# print(soup.prettify())