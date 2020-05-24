from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import searchCardForm, searchCardNavForm, saveCardForm, deleteCardForm
from users.models import Profile
import requests
import time


# Create your views here.
def index(request):
    if request.method == 'GET':
        form = searchCardForm(request.GET)
        if form.is_valid():
            return HttpResponseRedirect('/search-card/')
    else:
        form = searchCardForm()
    
    return render(request, 'application/index.html', {'form': form})


def howItWorks(request):
    return render(request, 'application/how-it-works.html')


def about(request):
    return render(request, 'application/about.html')


def contact(request):
    return render(request, 'application/contact.html')


def cardNotFound(request):
    if request.method == 'GET':
        form = searchCardNavForm(request.GET)
        if form.is_valid():
            return HttpResponseRedirect('/search-card/')
    else:
        form = searchCardNavForm()
    return render(request, 'application/card-not-found.html', {'form': form})




def searchCard(request):
    fuzzyName = request.GET.get('cardName', '')
    r = requests.get("https://api.scryfall.com/cards/search?q=" + fuzzyName)
    rJSON = r.json()
    time.sleep(0.1)
    r2 = requests.get("https://api.scryfall.com/cards/named?fuzzy=" + fuzzyName)
    r2JSON = r2.json()
    form1 = saveCardForm()
    form2 = deleteCardForm()
    

    if request.method == 'GET':
        form = searchCardNavForm(request.GET)
        if form.is_valid():
            if rJSON['object'] == 'error':
                if r2JSON['object'] == 'card':
                    return render(request, 'application/search-card.html', {'form': form, 'form1': form1, 'form2': form2, 'card': r2JSON})
                else:
                    return HttpResponseRedirect('/card-not-found/')
            elif rJSON['total_cards'] == 1:
                return render(request, 'application/search-card.html', {'form': form, 'form1': form1, 'form2': form2, 'card': rJSON['data'][0]})
            else:
                card_list_length = min(20, rJSON['total_cards'])
                return render(request, 'application/multi-search.html', {'form': form, 'form1': form1, 'form2': form2, 'n': card_list_length, 'total_cards': rJSON['total_cards'], 'cards': rJSON['data'][0:card_list_length]})
    elif request.method == 'POST' and form1.is_valid():
        form1 = saveCardForm(request.POST)
        form2 = deleteCardForm(request.POST)
        a = request.user.profile
        image_url = ""
        if r2JSON['object'] == 'card':
            for each in a.savedCards["cards"]:
                if r2JSON['name'] in each:
                    form = searchCardNavForm()
                    return render(request, 'application/search-card.html', {'form': form, 'form1': form1, 'form2': form2, 'card': r2JSON})
            if 'card_faces' in r2JSON:
                image_url = r2JSON['card_faces']['0']['image_uris']['border_crop']
            else:
                image_url = r2JSON['image_uris']['border_crop']
        a.savedCards["cards"].append([r2JSON['name'], image_url])
        a.save()
        return HttpResponseRedirect('/profile/')

    elif request.method == 'POST' and form2.is_valid():
        return HttpResponseRedirect('/card-not-found/')
        if r2JSON['object'] == 'card':
            for each in a.savedCards["cards"]:
                if r2JSON['name'] in each:
                    a.savedCards["cards"].remove(each)
            a.save()
            return HttpResponseRedirect('/profile/')
        else:
            form = searchCardNavForm()
            return render(request, 'application/search-card.html', {'form': form, 'form1': form1, 'form2': form2, 'card': r2JSON})

    else:
        form = searchCardNavForm()
    
        if rJSON['object'] == 'error':
            if r2JSON['object'] == 'card':
                return render(request, 'application/search-card.html', {'form': form, 'form1': form1, 'form2': form2, 'card': r2JSON})
            else:
                return HttpResponseRedirect('/card-not-found/')
        elif rJSON['total_cards'] == 1:
            return render(request, 'application/search-card.html', {'form': form, 'form1': form1, 'form2': form2, 'card': rJSON['data'][0]})
        else:
            card_list_length = min(20, rJSON['total_cards'])
            return render(request, 'application/multi-search.html', {'form': form, 'form1': form1, 'form2': form2, 'n': card_list_length, 'total_cards': rJSON['total_cards'], 'cards': rJSON['data'][0:card_list_length]})




def multiSearch(request):
    fuzzyName = request.GET.get('cardName', '')
    r = requests.get("https://api.scryfall.com/cards/search?q=" + fuzzyName)
    rJSON = r.json()
    time.sleep(0.1)
    r2 = requests.get("https://api.scryfall.com/cards/named?fuzzy=" + fuzzyName)
    r2JSON = r2.json()
    

    if request.method == 'GET':
        form = searchCardNavForm(request.GET)
        if form.is_valid():
            if rJSON['object'] == 'error':
                if r2JSON['object'] == 'card':
                    return render(request, 'application/search-card.html', {'form': form, 'card': r2JSON})
                else:
                    return HttpResponseRedirect('/card-not-found/')
            elif rJSON['total_cards'] == 1:
                return render(request, 'application/search-card.html', {'form': form, 'card': rJSON['data'][0]})
            else:
                card_list_length = min(20, rJSON['total_cards'])
                return render(request, 'application/multi-search.html', {'form': form, 'n': card_list_length, 'total_cards': rJSON['total_cards'], 'cards': rJSON['data'][0:card_list_length]})
    else:
        form = searchCardNavForm()
    
    if rJSON['object'] == 'error':
        if r2JSON['object'] == 'card':
            return render(request, 'application/search-card.html', {'form': form, 'card': r2JSON})
        else:
            return HttpResponseRedirect('/card-not-found/')
    elif rJSON['total_cards'] == 1:
        return render(request, 'application/search-card.html', {'form': form, 'card': rJSON['data'][0]})
    else:
        card_list_length = min(20, rJSON['total_cards'])
        return render(request, 'application/multi-search.html', {'form': form, 'n': card_list_length, 'total_cards': rJSON['total_cards'], 'cards': rJSON['data'][0:card_list_length]})
