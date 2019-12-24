from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("<h1>yeet</h1>")

def about(request):
    return HttpResponse('<h1>about yeet<h1>')