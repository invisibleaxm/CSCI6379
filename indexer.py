#!/usr/local/bin/python3


#
#
# http://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
import string

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

def index_document(filename):
    soup = BeautifulSoup(open('document_corpus/' + filename))
    [x.extract() for x in soup.findAll('script')]
    text = remove_puctuation(soup.getText())
    #text = soup.getText()
    terms = [i.lower() for i in text.split() if i not in stop]
    for term in terms:
        try:
            invindex[term][filename] = invindex[term][filename] + 1
        except:
            invindex[term][filename] = 1




#print(punctuation)



#print(st.stem("saying"))
#print(st.stem("going"))

#splitting (tokenizing) and removing stop words
#print(st.stem([i for i in text.split() if i not in stop]))
for i in range(1,100):
    index_document(str(i) + '.htm')





#for key, value in invindex.items():
#    try:
#        print(key,value)
#    except:
#        pass

print("Searching for keyword: research")
print(invindex["research"])
#parse_document('2.htm')

