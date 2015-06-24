#!/usr/local/bin/python3


#
#
# http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import csv
#from nltk.stem.lancaster import LancasterStemmer


from collections import defaultdict

invindex = defaultdict(dict)

stop = stopwords.words('english')
st = PorterStemmer


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


def index_document(id, filename, url):
    soup = BeautifulSoup(open(filename))
    [x.extract() for x in soup.findAll('script')]
    raw_text = soup.getText()
    text = remove_puctuation(raw_text)
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
            index_document(row['index'], row['filename'], row['url'])
            #print(row['index'], row['filename'], row['url'])
    print("Searching for keyword: research")
    print(invindex["research"])

    #for i in range(1,100):
     #   index_document(str(i) + '.htm')





#for key, value in invindex.items():
#    try:
#        print(key,value)
#    except:
#        pass


#parse_document('2.htm')

