#!/usr/local/bin/python3


#
#
# http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv
from docinfo import docinfo
#from nltk.stem.lancaster import LancasterStemmer


from collections import defaultdict

invindex = defaultdict(dict)

stop = stopwords.words('english')
st = PorterStemmer

document_table = {} #index of documents and their information


#f = open('document_corpus/1.htm', 'r')
# remove punctuation marks
def remove_puctuation(s):
    return s.translate({ord('!'): '', ord('"'): '', ord('#'): '', ord('$'): '',
                        ord(','): '', ord('('): '', ord(')'): '', ord('.'): '',
                        ord(':'): '', ord('-'): '', ord('&'): '', ord('>'): '',
                        ord('<'): '', ord(';'): '', ord('{'): '', ord('}'): '',
                        ord('/'): '', ord('*'): '', ord('='): '', ord('?'): '',
                        ord('@'): '', ord('^'): '', ord('_'): '',
                        ord('\''): ''  })



def index_document(id, filename):
    soup = BeautifulSoup(open(filename))
    [x.extract() for x in soup.findAll('script')]
    text = remove_puctuation(soup.getText())
    title = soup.title.contents[0]
    snip = text.split()[60:80]
    document_table[mydoc.id].title = title
    document_table[mydoc.id].snip = " ".join(snip)
    #text = soup.getText()
    terms = [i.lower() for i in text.split() if i not in stop]
    for term in terms:
        try:
            invindex[term][str(id)] = invindex[term][str(id)] + 1
        except:
            invindex[term][str(id)] = 1






#print(punctuation)



#print(st.stem("saying"))
#print(st.stem("going"))

#splitting (tokenizing) and removing stop words
#print(st.stem([i for i in text.split() if i not in stop]))

if __name__ == '__main__':
    with open('crawled_files.txt', 'r') as inputfile:
        reader = csv.DictReader(inputfile)
        for row in reader:
            mydoc = docinfo()
            mydoc.id = row['index']
            mydoc.filename = row['filename']
            mydoc.url = row['url']
            document_table[mydoc.id] = mydoc
            index_document(mydoc.id, mydoc.filename)
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

