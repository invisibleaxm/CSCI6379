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
start_url = 'http://portal.utpa.edu/utpa_main/daa_home/coecs_home/cs_home'
base_os_dir = os.getcwd()+"/document_corpus"

#start_url = 'https://my.utpa.edu/home'

links = []

# # # # # # # # # # # # # # # # # 
# Simple function that will help "normalize" links. In other words, this function wil prepend the
# base_url if needed.
# # # # # # # # # # # # # # # # # #
def get_url(link):
    if(link[0]=='/'):
        return start_url+link
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
    elif re.match(r'(.*)utpa.edu(.*?)',link):
        return True
    else:
#        print("Not allowed: "+link)
        return False

def follow_links(html_page):
    bs = BeautifulSoup(html_page)
    try:
        for link in bs.find_all("a", href=re.compile('^http://|^/')) :
            if link.has_attr('href') and is_domain_allowed(link['href']):
                my_url = get_url(link["href"])
                if my_url not in links:
                    links.append(my_url)
        #print(links)
                    get_html(my_url)
                #print(get_url(link["href"]))
                # print(link["href"])
    except:
        pass


def get_html(url):
    try:
        #print("Following URL: ", url)
        #headers = { 'User-Agent' : 'Mozilla/5.0' }
        #req = Request(url, None, headers)
        #page = urlopen(req).read()
        my_headers = { 'User-Agent': 'Mozilla/5.0' }
        page = requests.get(url, headers = my_headers).text
        folder_structure = urlparse(url)
        os_folderstructure = base_os_dir + folder_structure.path.rsplit('/',1)[0]
        filename = url.split('/')[-1].split('#')[0].split('?')[0]
        if "." not in filename:
            filename = filename + ".html"
        if not os.path.exists(os_folderstructure):
            os.makedirs(os_folderstructure,exist_ok=True)
        full_filename = os.path.join(os_folderstructure + "/" + filename)
        

        print(os_folderstructure)
        print("Using Filename: " , filename)
        #print(page)
        if filename != ".html":
            with open(full_filename, 'w') as f:
                f.write(page)
        follow_links(page)
    except:
        print("Couldnt open page: ", url)
        raise
        #traceback.print_exc(file=sys.stdout)
        #pass



get_html(start_url)
