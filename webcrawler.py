#!/usr/local/bin/python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CSCI 6379: Information Retrieval
# Instructor: Dr. Chen
# Date: June 12, 2015
# Group Project Members:
#   Alex Campos
#   name
#   name
#   name
#
# Description:
# This program is a small web crawler that will be used to build a document
# corpus for our search engine. This document corpus will be constructed by
# following a "start_url" and then follow all links iff they are part of the
# "allowed_domains" which in turn will recursevly call the function to keep
# downloading all links until done.
# the downloaded documents will be kept in the directory "document_corpus"
# and will be named after the full URL of the original file location (to avoid
# file colisions).
#
#
# Credits:  This program was in part created by following the tutorial from
# the book "Violent Python by TJ O'Connor (ISBN: 978-1-59749-957-6)" As well
# as some web resources and lots of googling around:
# http://stackoverflow.com/questions/163009/urllib2-file-name
# http://stackoverflow.com/questions/29717424/python-converting-url-into-directory
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#from urllib.request import urlopen
#from urllib.request import Request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sys, traceback
import shutil
import os
import re

#start_url = 'http://portal.utpa.edu/utpa_main/daa_home/coecs_home/cs_home'
#start_url = 'http://portal.utpa.edu/utpa_main/daa_home/coecs_home/cs_home'
#start_url = 'https://my.utpa.edu/home'

#start webpage of our crawler
start_url = 'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources'

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
max_links = 4

create_subfolders = False



# # # # # # # # # # # # # # # # #
# Simple function that will help "normalize" links. In other words, this function wil prepend the
# base_url if needed.
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
# This function simply checks if the domain of the link is allowed (a.k.a. white listed
# if it is not, then the program will skip the link
# # # # # # # # # # # # # # # # # # # # # # # # #
def is_domain_allowed(link):
    if(link=="/"):
        return False
    elif(link[0]=='/'):
        return True
    elif re.match(r'(.*)dmoz.org(.*?)',link):
        return True
    else:
#        print("Not allowed: "+link)
        return False

def follow_links(html_page, base_url):
    bs = BeautifulSoup(html_page)
    try:
        for link in bs.find_all("a", href=re.compile('^http://|^/')) :
            if link.has_attr('href') and is_domain_allowed(link['href']) and len(links) < max_links:
                my_url = get_url(link["href"], base_url)
                if my_url not in links and my_url not in bad_links:
                    get_html(my_url)

    except:
        traceback.print_exc(file=sys.stdout)


def get_html(url):
    try:
        my_url = get_url(url, url)
        if my_url not in links and my_url not in bad_links:
            print("Following URL: ", url)
       	    my_headers = { 'User-Agent': 'Mozilla/5.0' }
            r = requests.get(url, headers = my_headers)
            if r.status_code == requests.codes.ok:
                page = r.text
                filename = url.split('/')[-1].split('#')[0].split('?')[0]
                if "." not in filename:
                    filename = filename + ".html"
                if create_subfolders == True: #does the user prefer to create folder structure based on url parsing?
                    folder_structure = urlparse(url)
                    os_folderstructure = base_os_dir + folder_structure.path.rsplit('/',1)[0] ## add folder names from url
       	            if not os.path.exists(os_folderstructure):
                        os.makedirs(os_folderstructure,exist_ok=True)
                        full_filename = os.path.join(os_folderstructure + "/" + filename)
                else:
                    full_filename = base_os_dir + "/" + filename
                #print(os_folderstructure)
                print("Using Filename: " , filename)
                #print(page)
                if filename != ".html":
                    try:
                        with open(full_filename, 'w') as f:
                            f.write(page)
                            links.append(my_url)
                            print("Successfully fetched url {} now we are about to follow it's links".format(my_url))
                            if len(links) < max_links: ## make this a parameter
                                follow_links(page, my_url)
                    except:
                        print("There was an error writing to file, flagging this page {} as bad".format(my_url))
                        bad_links.append(my_url)
                        os.remove(full_filename) #do some cleanup
            else:
                bad_links.append(my_url)
                print("Page couldnt be fetched. Response with status code {} ".format(r.status_code))
        else:
            print("Skipping URL: {} since we have been here before".format(my_url))
    except:
#        print("Couldnt open page: ", url)
        raise
        #traceback.print_exc(file=sys.stdout)
        #pass

if __name__ == '__main__':
    print("Welcome to CSCI 6370 web crawler")
    get_html(start_url)
    print("Total number of documents retrieved: {} ".format(len(links)))
    #print(links)
    print("Total number of bad documents: {}".format(len(bad_links)))
    #print(bad_links)
