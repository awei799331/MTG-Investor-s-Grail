from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import searchCardForm
import requests

# Create your views here.
def index(request):
    if request.method == 'GET':
        form = searchCardForm(request.GET)
        if form.is_valid():
            data = form.cleaned_data['cardName']
            print(data)
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


def searchCard(request):
    fuzzyName = request.GET.get('cardName', '')
    r = requests.get("https://api.scryfall.com/cards/named?fuzzy=" + fuzzyName)
    rJSON = r.json()
    if rJSON['object'] == 'error':
        return HttpResponse("<h1>go away</h1>")
    else:
        return render(request, 'search-card.html', {'fuzzyName': fuzzyName, 'name': rJSON['name'], 'imageUri': rJSON['image_uris']['border_crop']})