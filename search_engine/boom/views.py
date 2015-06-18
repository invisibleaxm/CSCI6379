from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
#some of this was written with the help of this online resource:
#http://www.bogotobogo.com/python/Django/Python_Django_hello_world_templates.php

# Create your views here.
def home(request):
    return render_to_response("base.html", { "QueryString" : "none"})

def search(request, query):
    return render_to_response("base.html", { "QueryString" : query})

