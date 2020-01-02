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
    r = requests.get("https://api.scryfall.com/cards/search?q=" + fuzzyName)
    rJSON = r.json()
    
    if rJSON['object'] == 'error':
        return HttpResponseRedirect('/card-not-found/')
    else:
        if request.method == 'GET':
            form = searchCardNavForm(request.GET)
            if form.is_valid():
                if rJSON['total_cards'] == 1:
                    return render(request, 'search-card.html', {'form': form, 'card': rJSON['data'][0]})
                else:
                    card_list_length = min(10, rJSON['total_cards'])
                    return render(request, 'multi-search.html', {'form': form, 'n': range(card_list_length),'cards': rJSON['data'][0:card_list_length]})
        else:
            form = searchCardForm()
        
        if rJSON['total_cards'] == 1:
            return render(request, 'search-card.html', {'form': form, 'card': rJSON['data'][0]})
        else:
            card_list_length = min(10, rJSON['total_cards'])
            return render(request, 'multi-search.html', {'form': form, 'n': range(card_list_length), 'cards': rJSON['data'][0:card_list_length]})


def multiSearch(request):
    fuzzyName = request.GET.get('cardName', '')
    r = requests.get("https://api.scryfall.com/cards/search?q=" + fuzzyName)
    rJSON = r.json()

    if rJSON['object'] == 'error':
        return HttpResponseRedirect('/card-not-found/')
    else:
        if request.method == 'GET':
            form = searchCardNavForm(request.GET)
            if form.is_valid():
                if rJSON['total_cards'] == 1:
                    return render(request, 'search-card.html', {'form': form, 'card': rJSON['data'][0]})
                else:
                    card_list_length = min(10, rJSON['total_cards'])
                    return render(request, 'multi-search.html', {'form': form, 'n': range(card_list_length),'cards': rJSON['data'][0:card_list_length]})
        else:
            form = searchCardForm()
        

        if rJSON['total_cards'] == 1:
            return render(request, 'search-card.html', {'form': form, 'card': rJSON['data'][0]})
        else:
            card_list_length = min(10, rJSON['total_cards'])
            return render(request, 'multi-search.html', {'form': form, 'n': range(card_list_length), 'cards': rJSON['data'][0:card_list_length]})