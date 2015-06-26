from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
#import socket
from docinfo import docinfo
import json
import struct
import socket



reference_table = {}


# Following functions were "borrowed" from information comming
# from these sites
# http://stackoverflow.com/questions/13979764/python-converting-sock-recv-to-string
# http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
def send_msg(sock,msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack(b'>I', len(msg)) + msg.encode('utf-8', 'ignore')
    #print(msg)
    sock.sendall(msg)

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

# # # # # # # # # # # # #
# Load document refrence table from disk (a json) into memory
# # # # # # # # # # #
def read_document_reference():
    with open('document_reference.json') as data_file:
        data = json.load(data_file)
    for e in data:
        mydoc = docinfo()
        mydoc.id = e['id']
        mydoc.filename = e['filename']
        mydoc.url = e['url']
        mydoc.title = e['title']
        mydoc.snip = e['snip']
        reference_table[mydoc.id] = mydoc

#some of this was written with the help of this online resource:
#http://www.djangobook.com/en/2.0/chapter07.html

# Create your views here.
def search(request):
    #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('localhost',9999))
    result_dict = {}
    if 'q' in request.GET:
        try:
            read_document_reference()
            send_msg(s,request.GET['q'])
            result_dict = {}
            data = ''
            data = recv_msg(s)
            for docid in data.split(','):
                refid = docid.split(':')[1]
                mydoc = docinfo()
                mydoc.id = refid
                mydoc.title = reference_table[refid].title.encode('cp850','replace').decode('cp850')
                mydoc.url = reference_table[refid].url.encode('cp850','replace').decode('cp850')
                mydoc.snip = reference_table[refid].snip.encode('cp850','replace').decode('cp850')
                result_dict[mydoc.id] = mydoc
                print(mydoc.id)
        except:
            s.close ()
            return render_to_response("base.html")
    else:
        return render_to_response("base.html")
     #   return render(request, 'search_form.html')
    s.close ()
    return render_to_response("base.html", { 'q' : result_dict })




def search_form(request):
    return render(request, 'search_form.html')


