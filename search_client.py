#! /usr/bin/python3
import socket
import struct
import json
from docinfo import docinfo

reference_table = {}

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',9999))

# Following functions were "borrowed" from information comming
# from these sites
# http://stackoverflow.com/questions/13979764/python-converting-sock-recv-to-string
# http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
def send_msg(msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack(b'>I', len(msg)) + msg.encode('utf-8', 'ignore')
    #print(msg)
    s.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack(b'>I', raw_msglen.encode('utf-8', 'ignore'))[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet.decode('utf-8','ignore')
    return data
### END OF BORROWED FUNCTIONS ###


def search(query):
    #s.send(query.encode('utf-8'))
    send_msg(query)
    data = ''
    data = recv_msg(s)
    #print(data)
    for docid in data.split(','):
        refid = docid.split(':')[1]
        print(reference_table[refid].title.encode('cp850','replace').decode('cp850'))
    #data = ''
    #data = s.recv(8000).decode('utf-8')

    #print(data)

def read_document_reference():

    with open('document_reference.json') as data_file:
        data = json.load(data_file)
    print(type(data[0]))
    print(data[0]["id"])
    for e in data:
        mydoc = docinfo()
        mydoc.id = e['id']
        mydoc.filename = e['filename']
        mydoc.url = e['url']
        mydoc.title = e['title']
        mydoc.snip = e['snip']
        reference_table[mydoc.id] = mydoc
        #print(mydoc.id)


read_document_reference()
search("clear OR student")


s.close ()
