import requests
from bs4 import BeautifulSoup
import csv
from langdetect import detect

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


def get_outlinks(links, language):
    outlinks = []
    for link in links:
        if 'href' in link.attrs:
            if 'https://' in link['href'] or 'http://' in link['href']:
                if link['href'] not in outlinks:
                    if get_language(link['href']) == language:
                        outlinks.append(link['href'])
                        print('added')
    return outlinks


def get_language(seed) -> str:
    try:
        req = requests.get(seed)
    except:
        return 'language could not be found, GET request failed'
    soup = BeautifulSoup(req.text, "html.parser")
    try:
        language = detect(soup.get_text())
        print(soup.title.string)
        print(language)
        return language
    except:
        return 'no language detected'


def creepy_crawler(link, language):
    # print(link)
    # GET request on seed
    req = requests.get(link)

    # Get the link as BeautifulSoup object
    soup = BeautifulSoup(req.text, "html.parser")

    # Create a new file and save in repository folder
    add_to_repository(req.text)

    # Get all links for seed
    outlinks = get_outlinks(soup('a'), language)
    all_links.extend(
        [outlink for outlink in outlinks if outlink not in all_links])

    # Add seed to report.csv
    add_to_report(link, len(outlinks))

    global counter
    if counter > 500:
        return "done"
    else:
        creepy_crawler(all_links.pop(0), language)


# seed = "https://disney.fandom.com/wiki/The_Disney_Wiki"
seed = "https://www.yahoo.co.jp/"
language = get_language(seed)
print('Seed:', seed)
print('Language:', language, '\n')

creepy_crawler(seed, language)
