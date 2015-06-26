#!/usr/local/bin/python3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# CSCI 6379: Information Retrieval
# Instructor: Dr. Chen
# Date: June 25, 2015
# Search Engine: Boom
# Group Project Members: Alex Campos, Alvaro Leal, Akhil Ch, Divya Vuppala
#
# Description:
# This program parses each document downloaded by our web
# crawler and will apply a couple of nltk algorithms to
# remove the stop words, punctuation characters, <script>
# tags and then build an inverted index (bag of words)
# at this stage of our project, this indexer also asks the
# user for a search query although the plan is to change
# this behavior next phase and start using our WEB GUI
#
# Credits:  A lot of the more complex algorithms being used
# are actually from python libraries like the natural lang.
# toolkit (http://www.nltk.org/) which provides our stopword
# removal as well as our Stemmer algorithm
# http://tuhrig.de/extracting-meaningful-content-from-raw-html/
# http://stackoverflow.com/questions/13979764/python-converting-sock-recv-to-string
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv
from docinfo import docinfo
from collections import defaultdict
import socketserver
# invindex defines a 2 dimentional dictionary (hash table) which holds our
# inverted document index. We chosed a dictionary data structure for its
# fast searches and updates.
invindex = defaultdict(dict)

# get a list of all enfglish stop words provided by the nltk library
stop = stopwords.words('english')

st = PorterStemmer

document_table = {} #index of documents and their information

# function copied with minor modifications from:
# http://stackoverflow.com/questions/13979764/python-converting-sock-recv-to-string
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(1024)
            if not self.data:
                print('DISCONNECTED')
                break
            terms = []
            search_results = {}
            msg = ""
            search_query = self.data.decode('utf-8')
            print('RECEIVED: ' + search_query)
            search_terms = search_query.split()
            if len(search_terms) == 1:
                terms.append(search_terms[0])
                search_results = do_search(terms, None)

            else:
                for keyword in search_terms:
                    if keyword == "OR" or keyword == "AND" or keyword == "BUT":
                        operation = keyword
                    else:
                        terms.append(keyword)
                search_results = do_search(terms,operation)
            for k, v in search_results.items():
                msg += "Docid: {0} : {1}\n".format(k, document_table[k].url)
            self.request.sendall(msg.encode('utf-8'))




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Description: This function takes advantage of a string function in
# which takes an ascii map as input and translates each
# ordinal value with the requested character. In this case
# we are replacing each punctuation markwith the empty char
# input parameters: The string (s) that needs to have it's
# punctuation characters removed
# return value: string s with no special characters
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def remove_puctuation(s):
    return s.translate({ord('!'): '', ord('"'): '', ord('#'): '', ord('$'): '',
                        ord(','): '', ord('('): '', ord(')'): '', ord('.'): '',
                        ord(':'): '', ord('-'): '', ord('&'): '', ord('>'): '',
                        ord('<'): '', ord(';'): '', ord('{'): '', ord('}'): '',
                        ord('/'): '', ord('*'): '', ord('='): '', ord('?'): '',
                        ord('@'): '', ord('^'): '', ord('_'): '',
                        ord('\''): ''  })


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Description: Given a filename and its numeric identifies, removes the html
# tags, removes stop words, and tokenizes the file into meaningful words by
# removing english stop words. It then extracts the page title and the page snip
# that is then added to our "document_table" data structurewhich is nothing
# more thana lookup table that is used to retrieve document metadata
def index_document(id, filename):
    #we get the file from disk and initialize an html parsing library with it
    soup = BeautifulSoup(open(filename))

    #remove all the text inside every <script> tag
    #[x.extract() for x in soup.findAll('script')]
    map(lambda x: x.extract(), soup.findAll("code"))      # delete all
    map(lambda x: x.extract(), soup.findAll("style"))     # delete all
    map(lambda x: x.extract(), soup.findAll("script"))    # delete all

    #removes all the special punctuation
    text = remove_puctuation(soup.getText())
    #get title of document
    title = soup.title.contents[0]
    #get snippet of text (20 words from the middle of the text)
    snip = text.split()[60:80]
    #save the title and the snippet into the document_table (reference)
    document_table[mydoc.id].title = title
    document_table[mydoc.id].snip = " ".join(snip)
    #text = soup.getText()
    #tokenize the page into words separated by spaces
    terms = [i.lower() for i in text.split() if i not in stop]
    for term in terms:
        try:
            invindex[term][str(id)] = invindex[term][str(id)] + 1
        except:
            invindex[term][str(id)] = 1




def do_search(myterms, operator):
    termA = {}
    #termB = {}
    termResults = {}
    print("Searching for: " + " ".join(myterms) + " using operator {}".format(operator))
    if len(myterms) == 1 and operator is None:
        termResults = invindex[myterms[0]]
    else:
        termA = invindex[myterms[0]]
        termB = invindex[myterms[1]]
        if operator == "OR":
            termResults = termA.copy()
            termResults.update(termB)
        if operator == "AND":
            for k, v in termA.items():
                if k in termB.keys():
                    termResults[k] = v
        if operator == "BUT":
            for k, v in termA.items():
                if k not in termB.keys():
                    termResults[k] = v

    #merge both dictionaries

   # print("\nThe following files match your query string")
   # print("\n*******************************************")
   # for k, v in termResults.items():
   #         print("Document {0} : {1}".format(k, document_table[k].url))
   # print("\nTotal documents found : {0}".format(len(termResults)))
   # print("\n*******************************************")
    return termResults

#print(punctuation)



#print(st.stem("saying"))
#print(st.stem("going"))

#splitting (tokenizing) and removing stop words
#print(st.stem([i for i in text.split() if i not in stop]))

if __name__ == '__main__':
    print("Indexing 100 documents, please wait a few seconds.")
    with open('crawled_files.txt', 'r') as inputfile:
        reader = csv.DictReader(inputfile)
        for row in reader:
            mydoc = docinfo()
            mydoc.id = row['index']
            mydoc.filename = row['filename']
            mydoc.url = row['url']
            document_table[mydoc.id] = mydoc
            index_document(mydoc.id, mydoc.filename)
    print("Now accepting queries...")
    server = socketserver.TCPServer(('localhost', 9999), MyTCPHandler)
    server.serve_forever()

   # while True:
   #     terms = []
   #     search_query = input("Enter search term or quit to exit: ")
   #     if search_query == "quit":
   #         break
   #     else:
   #         search_terms = search_query.split()
   #         if len(search_terms) == 1:
   #             terms.append(search_terms[0])
   #             do_search(terms, None)
   #         else:
   #             for keyword in search_terms:
   #                 if keyword == "OR" or keyword == "AND" or keyword == "BUT":
   #                     operation = keyword
   #                 else:
   #                     terms.append(keyword)
   #             do_search(terms,operation)




        #    #print(row['index'], row['filename'], row['url'])
    #print("Searching for keyword: research")
    #print(invindex["research"])
    #print(document_table['2'].filename)

    #for i in range(1,100):
     #   index_document(str(i) + '.htm')





#for key, value in document_table.items():
#    try:
#        print(value.id, value.snip)
#    except:
#        pass


#parse_document('2.htm')

