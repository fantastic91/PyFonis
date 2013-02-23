# Create your views here.
from django.shortcuts import render_to_response
import django.shortcuts
from django.template import RequestContext, Template
from aplikacija.models import Projekti, Clan
from django.http import HttpResponse
from aplikacija.forms import DodavanjeProjekta, DodajClana, DodavanjeProjektaModel, DodajClanaModel
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory


def provjera_logina(view):
    def novi_view(request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request)
    return novi_view


def projekat(request, projekat_id):
  podaci = Projekti.objects.filter(id=projekat_id)
  return render_to_response('projekat.html', {'podaci':podaci}, context_instance=RequestContext(request))

def clan_prikaz(request, clan_id):
  podaci = Clan.objects.filter(id=clan_id)
  return render_to_response('clan_prikaz.html', {'podaci':podaci}, context_instance=RequestContext(request))

def clan_prikaz_edit(request, clan_id):
  clan_za_edit = Clan.objects.get(pk=clan_id)
  if request.method == 'POST':
    form = DodajClanaModel(request.POST, instance=clan_za_edit)
    if form.is_valid():
      try: 
        form.save()
        return HttpResponseRedirect('/clan/upisano/')
      except: 
        return HttpResponseRedirect('/clan/')
      
  else:
    form = DodajClanaModel(instance=clan_za_edit)
  podaci = Clan.objects.filter(id=clan_id)
  return render_to_response('clan_edit.html', {'podaci':podaci , 'form':form}, context_instance=RequestContext(request))


def projekat_delete(request, projekat_id):
  projekat_za_delete = Projekti.objects.get(pk=projekat_id)
  projekat_za_delete.delete()
  return HttpResponseRedirect('/upis/obrisano/')

def projekat_obrisano(request):
  return render_to_response('projekat_obrisano.html', context_instance=RequestContext(request))

def clan_delete(request, clan_id):
  clan_za_delete = Clan.objects.get(pk=clan_id)
  clan_za_delete.delete()
  return HttpResponseRedirect('/clan/obrisano/')

def clan_obrisano(request):
  return render_to_response('clan_obrisano.html', context_instance=RequestContext(request))
    
def projekat_edit(request, projekat_id):
  projekat_za_edit = Projekti.objects.get(pk=projekat_id)
  if request.method == 'POST':
    form = DodavanjeProjektaModel(request.POST, instance=projekat_za_edit)
    if form.is_valid():
      try: 
        form.save()
        return HttpResponseRedirect('/upis/upisano/')
      except: 
        return HttpResponseRedirect('/projekti/prikaz/')
      
  else:
    form = DodavanjeProjektaModel(instance=projekat_za_edit)
  podaci = Projekti.objects.filter(id=projekat_id)
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
            upis_projekti.save()
            izabrani_clanovi = cd['izaberi_clanove']
            for check in izabrani_clanovi:
               upis_projekti.ukljuceni_clanovi.add(check)
            return HttpResponseRedirect('/upis/upisano/')
    else:
        form = DodavanjeProjekta()
    clanovi = Clan.objects.all()
    return render_to_response('upis.html', {'form': form, 'clanovi':clanovi}, context_instance=RequestContext(request))
	
	
	
	
def pretraga_forma(request):
	return render_to_response('pretraga-forma.html', context_instance=RequestContext(request))

def upis_upisano(request):
	return render_to_response('upis_upisano.html', context_instance=RequestContext(request))
def clan_upisano(request):
  return render_to_response('clan_upisano.html', context_instance=RequestContext(request))

def pretraga(request):
	greska = False
	if 'q' in request.GET:
		q = request.GET['q']
		if not q:
			greska = True
		elif len(q) > 20:
			greska = True
		else: 
			projekti = Projekti.objects.filter(naziv__icontains=q) or Projekti.objects.filter(opis__icontains=q) or Projekti.objects.filter(sala__icontains=q)
			return render_to_response('rezultati_pretrage.html', {'projekti':projekti, 'query':q}, context_instance=RequestContext(request))
	return render_to_response('pretraga-forma.html', {'greska': greska}, context_instance=RequestContext(request))
		

def clan_dodaj(request):
	clan = Clan.objects.all()
	#podaci = Projekti.objects.get(id=4)
	#rjecnik = Clan.objects.get(id=1)
	#podaci.ukljuceni_clanovi.add(rjecnik)
	#listap = Projekti.objects.get(id=4)
	#ukupno = listap.ukljuceni_clanovi.all()
        if request.method == 'POST':
          form = DodajClana(request.POST)
          if form.is_valid():
            cd = form.cleaned_data
            upis_clan = Clan(ime=cd['ime_clana'], prezime=cd['prezime_clana'], email=cd['email_clana'])
            upis_clan.save()
            return HttpResponseRedirect('/clan/upisano/')
        else: 
          form = DodajClana()
	return render_to_response('clan_dodaj.html', {'form':form}, context_instance=RequestContext(request))
	#userAgent = request.META.get('HTTP_USER_AGENT', 'Greska')
	#return HttpResponse('Dobrodosli na %s' % userAgent)
        

def day_archive(request, year, month, day):
	date = datetime.date(int(year), int(month), int(day))
	projekti = Projekti.objects.filter(datum_pocetak=date)
	return render_to_response('datum.html', {'projekti':projekti}, context_instance=RequestContext(request))