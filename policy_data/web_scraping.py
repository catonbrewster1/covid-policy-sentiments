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
#index_dict = {}
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


