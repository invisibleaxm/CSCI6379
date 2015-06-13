#!python3
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

from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import re

#start_url = 'http://portal.utpa.edu/utpa_main/daa_home/coecs_home/cs_home'
start_url = 'http://portal.utpa.edu/utpa_main/daa_home/coecs_home/cs_home'
base_dir = os.getcwd()
#start_url = 'https://my.utpa.edu/home'

links = []


def get_url(link):
    if(link[0]=='/'):
        return start_url+link
    else:
        return link

def is_domain_allowed(link):
#allowed domain is represented as a regular expression string.

    if(link=="/"):
        return False
    elif(link[0]=='/'):
        return True
    elif re.match(r'(.*)utpa.edu(.*?)',link):
        return True
    else:
#        print("Not allowed: "+link)
        return False
   # if any(link in s for s in allowed_domains):
   #     return True




def follow_links(html_page):
    bs = BeautifulSoup(html_page)
    try:
        for link in bs.find_all("a", href=re.compile('^http://|^/')) :
            if link.has_attr('href') and is_domain_allowed(link['href']):
                my_url = get_url(link["href"])
                if my_url not in links:
                    links.append(my_url)
                    #get_html(my_url)
                    print("recursive..")
                #print(get_url(link["href"]))
                # print(link["href"])
    except:
        pass


def get_html(url):
    try:
        print("Following URL: ", url)
        headers = { 'User-Agent' : 'Mozilla/5.0' }
        req = Request(url, None, headers)
        page = urlopen(req).read()
        folder_structure = urlparse(url)
        filename = url.split('/')[-1].split('#')[0].split('?')[0]
        print("Using Filename: " , filename)
        follow_links(page)
    except:
        print("Couldnt open page: ", url)
        pass



get_html(start_url)
