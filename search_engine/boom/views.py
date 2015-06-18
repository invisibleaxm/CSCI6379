from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
#some of this was written with the help of this online resource:
#http://www.djangobook.com/en/2.0/chapter07.html

# Create your views here.
def search(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return render_to_response("base.html", { "q" : message})

#def search(request, query):
#  return render_to_response("base.html", { "QueryString" : query})



def search_form(request):
    return render(request, 'search_form.html')


