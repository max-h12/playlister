from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from .scripts import main as m

def index(request):
    return render(request, 'index.html')

def findPlaylist(request):
    url = request.GET['purl']
    oput = m.calculate(url)
    if(oput==-1):
        return index(request)
    return render(request, 'results.html', {"data":oput})

def argon(request):
    return render(request, 'argon.html')
