# CSCI6379
# Description:
This program is a small web crawler that will be used to build a document corpus for our search engine. This document corpus will be constructed by # following a "start_url" and then follow all links iff they are part of the "allowed_domain" which in turn will recursevly call the function to keep downloading all links until done.

The downloaded documents will be kept in the directory "document_corpus" and will be named after the full URL of the original file location (to avoid file colisions).


Credits:  This program was in part created by following the tutorial from the book "Violent Python by TJ O'Connor (ISBN: 978-1-59749-957-6)" As well as some web resources:
* http://docs.python-requests.org/en/latest/
* http://www.crummy.com/software/BeautifulSoup/bs4/doc/
* http://stackoverflow.com/questions/163009/urllib2-file-name
* http://stackoverflow.com/questions/29717424/python-converting-url-into-directory


