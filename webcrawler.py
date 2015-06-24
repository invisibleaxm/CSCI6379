#!/usr/local/bin/python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CSCI 6379: Information Retrieval
# Instructor: Dr. Chen
# Date: June 12, 2015
# Search Engine: Boom
# Group Project Members: Alex Campos, Alvaro Leal, Akhil Ch, Divya Vuppala
#
# Description:
# This program is a small web crawler that will be used to build a document
# corpus for our search engine. This document corpus will be constructed by
# following a "start_url" and then follow all links iff they are part of the
# "allowed_domain" which in turn will recursevly call the function to keep
# downloading all links until done.
# the downloaded documents will be kept in the directory "document_corpus"
# and will be named after the full URL of the original file location (to avoid
# file colisions).
#
#
# Credits:  This program was in part created by following the tutorial from
# the book "Violent Python by TJ O'Connor (ISBN: 978-1-59749-957-6)" As well
# as some web resources:
# http://docs.python-requests.org/en/latest/
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys, traceback, os, re

#where to start our crawling
start_url = 'http://cs.utpa.edu/'

#where to store the files a.k.a. document corpus.
base_os_dir = os.getcwd()+"/document_corpus"

# this list data structure will keep track of all "good" urls. By good we mean
# documents that we were able to parse and save to disk
links = []

#this keeps track of the documents that returned page not found,
# documents we had no access or couldnt write to disk. This way we dont waste
# time trying to access them again
bad_links = []

#since we want to limit our crawler to a "small" document corpus, we define a
# variable that will limit the number of files fetched.
max_links = 100

# we do not want to crawl anything outside of utpa.edu so we define this here.
allowed_domain = "utpa.edu"

# table to save the filename, file id and file URL which will be used by the indexer on phase 2
crawled_files = {}

outfile = None


# # # # # # # # # # # # # # # # #
# This function returns an absolute URL. The reason is that some times when
# parsing a hyper-link we will come across a relative URL that needs the
# base url to function.
# # # # # # # # # # # # # # # # # #
def get_url(link, base_url):
    parsed_url = urlparse(base_url)
    if(link[0]=='/'):
        good_url = parsed_url.scheme + "://" + parsed_url.netloc +link
        #print("returning url: " + good_url)
        return good_url
    else:
        return link

# # # # # # # # # # # # # # # # # # # # # # # # #
# This function simply checks if the domain of the link is allowed (a.k.a.
# white listed if it is not, then the program will skip the link
# # # # # # # # # # # # # # # # # # # # # # # # #
def is_domain_allowed(link):
    if(link=="/"):
        return False
    elif(link[0]=='/'):
        return True
    elif re.match(r'(.*)' + allowed_domain+ '(.*?)',link):
        return True
    else:
        return False

# # # # # # # # # # # # # # # # # # # # # # # # # #
# This is a helper function that parses the page looking for all hyper links
# <a href="..."> tags and tries to download them to disk if and only if this is
# a brand new link and if we have not reached the max number of desired links
# # # # # # # # # # # # # # # # # # # # # # # # # #
def follow_links(html_page, base_url):
    bs = BeautifulSoup(html_page)
    try:
        #look at links that start with http or with / (absolute or relative)
        for link in bs.find_all("a", href=re.compile('^http://|^/')) :
            if link.has_attr('href') and is_domain_allowed(link['href']) and len(links) < max_links:
                my_url = get_url(link["href"], base_url)
                if my_url not in links and my_url not in bad_links:
                    get_html(my_url)
    except:
        traceback.print_exc(file=sys.stdout)

# # # # # # # # # # # # # # # # # # # # # # # # # #
# This function tries to download the web page from the web server into disk.
# It keeps a history of all the "good" and "bad" links on two separate lists
# to ensure that we only visit links that we have not seen before.
# Once this funtion is done fetching the page, it calls follow_links which in
# turns calls this function again making it a recursive call (for as long as
# we havent reached the maximum number of links needed on the document corpus
# # # # # # # # # # # # # # # # # # # # # # # # # #
def get_html(url):
    try:
        my_url = get_url(url, url)
        if my_url not in links and my_url not in bad_links:
            print("Following URL: ", url)
       	    my_headers = { 'User-Agent': 'Mozilla/5.0' }

            r = requests.get(url, headers = my_headers, allow_redirects=True)
            if len(r.history ) > 0: #follow one redirect only to avoid loops
                print("Found redirect, following {0} instead".format(r.url))
                url = r.url
                r = requests.get(url, headers = my_headers, allow_redirects=False)

            # only worry about html/text docs that return a success status code
            if r.status_code == requests.codes.ok and r.headers['content-type'].find('text/html') >=0:
                page = r.text
                # we build a filename based on the current size of the "links"
                # data structure. this way we avoid duplicate file names.
                # We can later on write this to disk so we have
                # a table with index, url etc if needed.
                i = str(len(links) + 1)
                full_filename = base_os_dir + "/" + i + ".htm"
                try:
                    with open(full_filename, 'w') as f:
                        f.write(page)
                        links.append(my_url)
                        crawled_files[full_filename] = my_url
                        outfile.write(str(i) + "," + full_filename + "," + my_url + "\n")
                        print("Success fetching: {} fetching next link:".format(my_url))
                        if len(links) < max_links: ## make this a parameter
                            follow_links(page, my_url)
                except:
                    print("There was an error writing to file, bad document: {}".format(my_url))
                    bad_links.append(my_url)
                    os.remove(full_filename) #do some cleanup
            else:
                bad_links.append(my_url)
                print("Page couldnt be fetched. Status code {0} with content-type {1} ".format(r.status_code, r.headers['content-type']))
        else:
            print("Skipping URL: {} since we have been here before".format(my_url))
    except:
        raise
        #traceback.print_exc(file=sys.stdout)
        #pass


# # # # # # # # # # # # # # # # # # # # # # # # # #
# Main function. A very simple/small function that calls the get_html function
# with the start_url defined. Once it finishes execution, it prints some statistics
# as to how many good/bad links were found during this pass
# # # # # # # # # # # # # # # # # # # # # # # # # #
if __name__ == '__main__':
    print("Welcome to CSCI 6370 web crawler")
    outfile = open('crawled_files.txt', 'w')
    outfile.write("index,filename,url\n")
    get_html(start_url)
    outfile.close()
    print("Total number of documents retrieved: {} ".format(len(links)))
    print("Total number of bad documents: {}".format(len(bad_links)))

    #with open('crawled_files.txt', 'w') as outfile:
    #    for k,v in sorted(crawled_files.items()):
    #        outfile.write(k + "," + v + "\n")
