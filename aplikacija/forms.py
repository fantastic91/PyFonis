from django import forms
from aplikacija.models import Projekti, Profil, UserPrikazImena, Sastanci
from random import choice
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.databrowse.plugins.calendars import CalendarPlugin
from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL.ImageFileIO import ImageFileIO

class DodavanjeSastanka(forms.Form):
    izaberi_projekat = forms.ModelChoiceField(queryset=Projekti.objects.all(), widget=forms.Select(attrs={'class':'forma'}))
    naziv = forms.CharField()
    prisutni_clanovi = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, queryset=UserPrikazImena.objects.filter(is_active='1'))
    datum = forms.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y.'])
    vrijeme = forms.TimeField()
    opis = forms.CharField(widget=forms.Textarea)

class DodavanjeProjekta(forms.Form):
    naziv_projekta = forms.CharField()
    izaberi_koordinatora = forms.ModelChoiceField(queryset=UserPrikazImena.objects.filter(is_active='1'), widget=forms.Select(attrs={'class':'forma'}))
    izaberi_clanove = forms.ModelMultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, queryset=UserPrikazImena.objects.filter(is_active='1'))
    sala = forms.CharField()
    datum_pocetak = forms.DateField(label='Datum pocetka', input_formats=['%d/%m/%Y', '%d.%m.%Y.'])
    datum_kraj = forms.DateField(label='Datum kraja', input_formats=['%d/%m/%Y', '%d.%m.%Y.'])
    opis = forms.CharField(widget=forms.Textarea)

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

class DodavanjeProjektaModel(ModelForm):
    class Meta:
      model = Projekti

class DodavanjeSastanka(ModelForm):
    datum_odrzavanja = forms.DateField(label='Datum', input_formats=['%d/%m/%Y', '%d.%m.%Y.', '%Y-%m-%d'])
    vrijeme_odrzavanja = forms.TimeField(label='Vreme')
    prisutni_clanovi = forms.ModelMultipleChoiceField(required=False, queryset=UserPrikazImena.objects.filter(is_active='1'))
    class Meta:
      model = Sastanci    
      
class DodajProfilModel(ModelForm):
    korisnik = forms.ModelChoiceField(queryset=UserPrikazImena.objects.filter(is_active='1'), widget=forms.Select(attrs={'class':'forma'}))
    slika = forms.ImageField()
    class Meta:
      model = Profil
             
class DodajProfilForma(forms.Form):
    korisnik = forms.ModelChoiceField(queryset=User.objects.filter(is_active='1'), widget=forms.Select(attrs={'class':'forma'}))
    slika = ImageField(upload_to='aplikacija/static/uploads/')

class Registracija(UserCreationForm):
    username = forms.CharField(label="Korisnicko ime", max_length=30)
    first_name = forms.CharField(label="Ime")
    last_name = forms.CharField(label="Prezime")
    email = forms.EmailField(label="E-mail")
    class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email')
      
class UserChangePrilagodjeno(UserChangeForm):
    username = forms.CharField(label="Korisnicko ime", max_length=30)
    first_name = forms.CharField(label="Ime")
    last_name = forms.CharField(label="Prezime")
    email = forms.EmailField(label="E-mail")
    class Meta:
      model = User
      fields = ('username', 'first_name', 'last_name', 'email')