from django import forms
from django.contrib.auth.models import User

class searchCardForm(forms.Form):
    cardName = forms.CharField(max_length=200, label=False,
    widget = forms.TextInput(attrs={'autocomplete': 'off',
    'maxlength': '200',
    'spellcheck': 'false',
    'id': 'getCard',
    'class' : 'inputText',
    }))

class searchCardNavForm(forms.Form):
    cardName = forms.CharField(max_length=200, label=False,
    widget = forms.TextInput(attrs={'autocomplete': 'off',
    'maxlength': '200',
    'spellcheck': 'false',
    'class' : 'navSearch',
    }))

class saveCardForm(forms.Form):
    pass

class deleteCardForm(forms.Form):
    pass
