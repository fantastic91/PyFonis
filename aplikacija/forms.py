from django import forms
from aplikacija.models import Clan, Projekti
from random import choice
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.databrowse.plugins.calendars import CalendarPlugin

class DodavanjeProjekta(forms.Form):
    naziv_projekta = forms.CharField()
    izaberi_koordinatora = forms.ModelChoiceField(queryset=Clan.objects.all(), widget=forms.Select(attrs={'class':'forma'}))
    izaberi_clanove = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, queryset=Clan.objects.all())
    sala = forms.CharField()
    datum_pocetak = forms.DateField(label='Datum pocetka');
    datum_kraj = forms.DateField(label='Datum kraja');
    opis = forms.CharField(widget=forms.Textarea); 

    def clean_opis(self):
      opis = self.cleaned_data['opis']
      if len(opis) < 10:
        raise forms.ValidationError('Opis je prekratak.')
      return opis
    
    def clean_naziv_projekta(self):
      naziv = self.cleaned_data['naziv_projekta']
      if Projekti.objects.filter(naziv__iexact=naziv):
        raise forms.ValidationError('Naziv projekta vec postoji u bazi')
      return naziv
    
class DodajClana(forms.Form):
    ime_clana = forms.CharField()
    prezime_clana = forms.CharField()
    email_clana = forms.CharField()
    
    def clean_email_clana(self):
      email = self.cleaned_data['email_clana']
      if Clan.objects.filter(email__icontains=email):
        raise forms.ValidationError('E-mail vec postoji u bazi!')
      return email
    
    