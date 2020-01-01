from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import searchCardForm, searchCardNavForm
import requests


# Create your views here.
def index(request):
    if request.method == 'GET':
        form = searchCardForm(request.GET)
        if form.is_valid():
            return HttpResponseRedirect('/search-card/')
    else:
        form = searchCardForm()
    
    return render(request, 'index.html', {'form': form})


def howItWorks(request):
    return render(request, 'how-it-works.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def cardNotFound(request):
    if request.method == 'GET':
        form = searchCardNavForm(request.GET)
        if form.is_valid():
            return HttpResponseRedirect('/search-card/')
    else:
        form = searchCardNavForm()
    return render(request, 'card-not-found.html', {'form': form})


def searchCard(request):
    fuzzyName = request.GET.get('cardName', '')
    r = requests.get("https://api.scryfall.com/cards/named?fuzzy=" + fuzzyName)
    rJSON = r.json()

    if rJSON['object'] == 'error':
        return HttpResponseRedirect('/card-not-found/')
    else:
        if request.method == 'GET':
            form = searchCardNavForm(request.GET)
            if form.is_valid():
                return render(request, 'search-card.html', {'form': form, 'fuzzyName': fuzzyName, 'card': rJSON})
        else:
            form = searchCardForm()
        return render(request, 'search-card.html', {'form': form, 'fuzzyName': fuzzyName, 'card': rJSON})