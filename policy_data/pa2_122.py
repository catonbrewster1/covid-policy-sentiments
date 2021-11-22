"""
CAPP 30122: Course Search Engine Part 1

Caton Brewster
"""
# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg=invalid-name, redefined-outer-name, unused-argument, unused-variable

import queue
import json
import sys
import csv
import re
import bs4
import util

INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                    'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet'])


def convert_url(url):
    '''
    Takes a URL and converts it to a Beautiful Soup object

    Input: (str) a URL
    Output: (BeautifulSoup obj)
    '''
    request = util.get_request(url)
    html = util.read_request(request)
    return bs4.BeautifulSoup(html, "html5lib")


def get_course_info(course, course_id_dict):
    '''
    Takes a BeautifulSoup tag associated with a course block and
    pulls out the information needed, including the course title,
    the course code, and the description of the course. Also pulls
    the course id associated with the given course code.

    Returns a tuple with the course id and a list which is the
    list of words that will be searched through to find valid words
    to associate with the given course code.

    Input:
        - course (BeautifulSoup tag)
        - course_id_dict (dictionary)
    Output (tuple): (str, list)
    '''

    title_section = course.find('p', class_ = "courseblocktitle")
    title_section_txt = title_section.text.replace('\xa0', ' ')
    desc_section = course.find('p', class_ = "courseblockdesc")
    desc_section_txt = desc_section.text.replace('\n', '')

    course_code = title_section_txt.split('.')[0]
    course_id = course_id_dict.get(course_code, None)

    return course_id, title_section_txt.split() + desc_section_txt.split()


def add_word_to_index(word, course_id, index_dict):
    '''
    Takes a word and course code and adds them to the indexing dictionary
    which tracks which courses a given word shows up in.

    Input:
        - word (str)
        - course_id (str)
        - index_dict (dictionary)

    Output (N/A): updates dictionary in place
    '''

    if word not in index_dict:
        index_dict[word] = []
    if course_id not in index_dict[word]:
        index_dict[word].append(course_id)


def add_course_to_index(text, course_id, index_dict):
    '''
    Takes a chunk of text and checks each word; if it's considered a valid 
    word,it is added to the indexing dictionary. Updates dictionary in 
    place.

    Inputs:
        - text (str)
        - course_id (str)
        - index_dict (dict)
    Outputs: N/A - updates index_dict dictionary in place

    Used https://docs.python.org/3/library/re.html for re fxns
    '''

    for word in text:
        l_word = re.sub('[!.,:]', '', word).lower()
        valid = l_word not in INDEX_IGNORE and \
                len(l_word) > 0 and \
                re.match("^[A-Za-z0-9_]*$", l_word) and \
                l_word[0].isalpha()
        if valid:
            add_word_to_index(l_word, course_id, index_dict)


def scrape_urls(tag, page_url, url_list, num_v, limiting_domain):
    '''
    Takes a url and if its valid, appends it to the url_list to
    visit. If appended, increments the number of pages visited
    counter.

    Input:
        - tag (BeautifulSoup tag)
        - page_url (str)
        - url_list (list)
        - num_v (int)
        - limiting_doman (int)

    Output: N/A updates url_list and num_v in place
    '''

    url = tag.get('href')
    if not util.is_absolute_url(url):
        url = util.convert_if_relative_url(page_url, url)
    url = util.remove_fragment(url)
    if url not in url_list and util.is_url_ok_to_follow(url, limiting_domain):
        url_list.append(url)
        num_v += 1


def go(num_pages_to_crawl, course_map_filename, index_filename):
    '''
    Crawl the college catalog and generates a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs:
        CSV file of the index index.

    for saving a csv file referenced: 
    https://www.tutorialspoint.com/How-to-save-a-Python-Dictionary-to-CSV-file
    '''

    with open(course_map_filename) as course_map:
        data = json.load(course_map)
    course_id_map = dict(data)

    limiting_domain = "classes.cs.uchicago.edu"
    starting_url = ("http://www.classes.cs.uchicago.edu/archive/2015/winter"
                    "/12200-1/new.collegecatalog.uchicago.edu/index.html")
    num_v = 0
    index_dict = {}
    url_list = [starting_url]

    for url in url_list:
        soup_page = convert_url(url)
        for tag in soup_page.find_all('a'):
            if tag.has_attr("href") and num_v < num_pages_to_crawl:
                #add urls to url_list
                scrape_urls(tag, url, url_list, num_v, limiting_domain)
        for tag in soup_page.find_all('div', class_ = "courseblock main"):
            #course
            subseq = util.find_sequence(tag)
            course_id, search_text = get_course_info(tag, course_id_map)
            if not subseq:
                #only add course to index dict if not a sequence
                add_course_to_index(search_text, course_id, index_dict)
            for sub in subseq:
                #add subseq info
                ss_course_id, ss_search_text = get_course_info(sub,
                                                               course_id_map)
                add_course_to_index(search_text + ss_search_text,
                                    ss_course_id, index_dict)

    with open(index_filename, 'w') as f:
        for word, course_lists in index_dict.items():
            for course in course_lists:
                f.write("%s|%s\n"%(course, word))


if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 1000
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)
        sys.exit(0)

    go(num_pages_to_crawl, course_map_filename, index_filename)
