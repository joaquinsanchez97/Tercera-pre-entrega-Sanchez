from django import forms

class formatraparPokemon(forms.Form):
    nivel = forms.IntegerField()
    nombre = forms.CharField(max_length=20)
    mote = forms.CharField(max_length=20)
