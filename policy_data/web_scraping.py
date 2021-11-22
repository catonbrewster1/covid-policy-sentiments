"""
Scrape State-Level Executive Order Data
"""

#Illinois
#Website: https://coronavirus.illinois.gov/resources/executive-orders.html

import queue
import json
import sys
import csv
import re
import bs4
import util


starting_url = ("https://coronavirus.illinois.gov/resources/executive-orders.html")
order_list = []
count = 0

soup_page = convert_url(starting_url)
for tag in soup_page.find_all('a'):
    if tag.has_attr("href"):
        url = tag.get('href')
        if url[0:10] == "/resources":
            url = "https://coronavirus.illinois.gov" + url
        if "executive-order" in url and "html" in url and \
            url not in order_list and "display" in url:
            page = convert_url(url)
            for tag_div in page.find_all('div', class_ = "cmp-text"):
                for tag_p in tag_div.find_all('p'):
                    #doesnt' seem to recognize text that I check for inside of tag_p...
                    if "Issued" in tag_p:
                        print(tag_p)
                    else:
                        print("Not in it: ")
                        print(tag_p)
                        print("")


with open(index_filename, 'w') as f:
    for word, course_lists in index_dict.items():
        for course in course_lists:
            f.write("%s|%s\n"%(course, word))


def convert_url(url):
    '''
    Takes a URL and converts it to a Beautiful Soup object

    Input: (str) a URL
    Output: (BeautifulSoup obj)
    '''
    request = util.get_request(url)
    html = util.read_request(request)
    return bs4.BeautifulSoup(html, "html5lib")


