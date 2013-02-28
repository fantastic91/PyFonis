# Create your views here.
from django.shortcuts import render_to_response
import django.shortcuts
from django.template import RequestContext, Template
from aplikacija.models import Projekti, Clan
from django.http import HttpResponse
from aplikacija.forms import DodavanjeProjekta, DodajClana, DodavanjeProjektaModel, DodajClanaModel
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django import template

def provjera_logina(view):
    def novi_view(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request)
    return novi_view


def opsti_response(request, template_name):
  return render_to_response(template_name, context_instance=RequestContext(request))

def handler404(request):
  response = details(request, 'novini')
  if response.status_code == '404':
    return render_to_response('404.html', context_instance=RequestContext(request))
  return render_to_response('404.html', context_instance=RequestContext(request))


def projekat(request, projekat_id):
  try: 
    podaci = Projekti.objects.get(id=projekat_id)
  except:
    return HttpResponseRedirect('/404/')
  broj_dana = podaci.datum_kraj - podaci.datum_pocetak
  now = date.today()
  status = False
  if now >= podaci.datum_pocetak and now <= podaci.datum_kraj:
    status = True
  return render_to_response('projekat.html', {'podaci':podaci, 'broj_dana':broj_dana, 'status':status}, context_instance=RequestContext(request))

def clan_prikaz(request, clan_id):
  try:
    podaci = Clan.objects.get(id=clan_id)
  except:
    return HttpResponseRedirect('/404/')
  return render_to_response('clan_prikaz.html', { 'podaci':podaci }, context_instance=RequestContext(request))

def clan_prikaz_edit(request, clan_id):
  try:
    clan_za_edit = Clan.objects.get(pk=clan_id)
  except:
    return HttpResponseRedirect('/404/')
  if request.method == 'POST':
    form = DodajClanaModel(request.POST, instance=clan_za_edit)
    if form.is_valid():
      try: 
        form.save()
        return HttpResponseRedirect('/clanovi/upisano/')
      except: 
        return HttpResponseRedirect('/greska/')      
  else:
    form = DodajClanaModel(instance=clan_za_edit)
  
  try:
    podaci = Clan.objects.get(id=clan_id)
  except:
    return HttpResponseRedirect('/greska/')      
  return render_to_response('clan_edit.html', {'podaci':podaci , 'form':form }, context_instance=RequestContext(request))

def projekat_delete(request, projekat_id):
  try:
    projekat_za_delete = Projekti.objects.get(pk=projekat_id)
  except:
    return HttpResponseRedirect('/404/')
  try: 
    projekat_za_delete.delete()
    return HttpResponseRedirect('/projekti/obrisano/')
  except:
    return HttpResponseRedirect('/greska/')

def clan_delete(request, clan_id):
  try:
    clan_za_delete = Clan.objects.get(pk=clan_id)
  except:
    return HttpResponseRedirect('/404/')
  try:
    clan_za_delete.delete()
    return HttpResponseRedirect('/clanovi/obrisano/')
  except:
    return HttpResponseRedirect('/greskao/')
  
def projekat_edit(request, projekat_id):
  try: 
    projekat_za_edit = Projekti.objects.get(pk=projekat_id)
  except:
    return HttpResponseRedirect('/404/')
  if request.method == 'POST':
    form = DodavanjeProjektaModel(request.POST, instance=projekat_za_edit)
    if form.is_valid():
      try: 
        form.save()
        return HttpResponseRedirect('/projekti/upisano/')
      except: 
        return HttpResponseRedirect('/greska/')
  else:
    form = DodavanjeProjektaModel(instance=projekat_za_edit)
  try:
    podaci = Projekti.objects.get(id=projekat_id)
  except:
    return HttpResponseRedirect('/greska/')
  return render_to_response('projekat_edit.html', {'podaci':podaci , 'form':form}, context_instance=RequestContext(request))

def accounts_login(request):
	return render_to_response('accounts_login.html', context_instance=RequestContext(request))

def clan(request):
  clanovi = Clan.objects.all()
  return render_to_response('clan.html', {'clanovi' : clanovi}, context_instance=RequestContext(request))

def home(request):
  podaci = Projekti.objects.all().order_by('id')
  return render_to_response('lista_projekata.html', {'Projekti' : podaci}, context_instance=RequestContext(request))

def upis(request):
    if request.method == 'POST':
        form = DodavanjeProjekta(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            upis_projekti = Projekti(
													naziv=cd['naziv_projekta'], 
													opis=cd['opis'], 
													koordinator=cd['izaberi_koordinatora'],
													datum_pocetak=cd['datum_pocetak'],
													datum_kraj=cd['datum_kraj'],
													sala=cd['sala'],
                          )
            try: 
              upis_projekti.save()
            except:              
              return HttpResponseRedirect('/greska/')
            izabrani_clanovi = cd['izaberi_clanove']
            for check in izabrani_clanovi:
               try:
                 upis_projekti.ukljuceni_clanovi.add(check)
               except:
                 return HttpResponseRedirect('/greska/')
            return HttpResponseRedirect('/projekti/upisano/')
    else:
        form = DodavanjeProjekta()
    clanovi = Clan.objects.all()
    return render_to_response('upis.html', {'form': form, 'clanovi':clanovi}, context_instance=RequestContext(request))
	
def pretraga(request):
  greska_duga = False
  greska_nema = False
  if 'q' in request.GET:
    q = request.GET['q']
  if not q:
    greska_nema = True
    return render_to_response('pretraga-forma.html', {'greska_nema': greska_nema}, context_instance=RequestContext(request))
  if len(q) > 30:
    greska_duga = True
    return render_to_response('pretraga-forma.html', {'greska_duga': greska_duga}, context_instance=RequestContext(request))
  else:
    projekti = Projekti.objects.filter(naziv__icontains=q) or Projekti.objects.filter(opis__icontains=q) or Projekti.objects.filter(sala__icontains=q)
    return render_to_response('rezultati_pretrage.html', {'projekti':projekti, 'query':q}, context_instance=RequestContext(request))
  return render_to_response('pretraga-forma.html', {'greska': greska}, context_instance=RequestContext(request))

def clan_dodaj(request):
  clan = Clan.objects.all()
  if request.method == 'POST':
    form = DodajClana(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      upis_clan = Clan(ime=cd['ime_clana'], prezime=cd['prezime_clana'], email=cd['email_clana'])
      try:
        upis_clan.save()
        return HttpResponseRedirect('/clanovi/upisano/')
      except:
        return HttpResponseRedirect('/greska/')
  else:
    form = DodajClana()
  return render_to_response('clan_dodaj.html', {'form':form}, context_instance=RequestContext(request))