# Create your views here.
from django.shortcuts import render_to_response
import django.shortcuts
from django.template import RequestContext, Template
from aplikacija.models import Projekti, Sastanci, Profil
from django.http import HttpResponse
from aplikacija.forms import DodavanjeProjekta, DodavanjeProjektaModel, DodajProfilModel, Registracija, DodajProfilForma, DodavanjeSastanka
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, Http404
from datetime import datetime, date
from django import template
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group

def registracija(request):
    if request.method == 'POST':
        form = Registracija(request.POST)
        if form.is_valid():
            novi = form.save()
            g = Group.objects.get(id='1') 
            g.user_set.add(User.objects.get(id=novi.id))
            return HttpResponseRedirect("/profil/kreiran/")
    else:
        form = Registracija()
    return render_to_response('profil/registracija.html', {'form': form}, context_instance=RequestContext(request))

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

def korisnik_edit(user):
    return user.is_authenticated() and user.has_perm("Delete_PS")

# =================================== PROJEKAT ===================================
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
  sastanci = Sastanci.objects.filter(projekat_id=projekat_id)
  return render_to_response('projekat/projekat.html', {'podaci':podaci, 'broj_dana':broj_dana, 'status':status, 'sastanci':sastanci}, context_instance=RequestContext(request))

@login_required
def projekat_add(request):
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
    clanovi = User.objects.filter(is_active='1')
    return render_to_response('projekat/projekat_dodaj.html', {'form': form, 'clanovi':clanovi}, context_instance=RequestContext(request))

@user_passes_test(korisnik_edit, login_url="/profil/login/")
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
  return render_to_response('projekat/projekat_edit.html', {'podaci':podaci , 'form':form}, context_instance=RequestContext(request))

@user_passes_test(korisnik_edit, login_url="/profil/login/")
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
# =================================== END PROJEKAT ===================================

# =================================== CLAN ===========================================
def clan(request):
  clanovi = User.objects.filter(is_active='1')
  return render_to_response('profil/clan.html', {'clanovi' : clanovi}, context_instance=RequestContext(request))

def clan_prikaz(request, clan_id):
  try:  
    podaci = User.objects.get(id=clan_id)
    slike = Profil.objects.get(korisnik_id=clan_id)
  except:
    slike = ''
  return render_to_response('profil/clan_prikaz.html', { 'podaci':podaci, 'slike':slike }, context_instance=RequestContext(request))

#@login_required
def profil(request):
  if request.user.is_authenticated():
    
    try:  
      podaci = User.objects.get(username=request.user.get_username())
    except:
      return HttpResponseRedirect('/greska/')
    try:
      slike = Profil.objects.get(korisnik_id=podaci.id)
    except:
      slike = ''
    return render_to_response('profil/profil.html', { 'podaci':podaci, 'slike':slike }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/404/')


@login_required
def profil_edit(request):
  if request.user.is_authenticated():
    try:
      clan_za_edit = User.objects.get(username=request.user.get_username())
    except:
      return HttpResponseRedirect('/404/')
    if request.method == 'POST':
      form = UserChangeForm(request.POST, instance=clan_za_edit)
      if form.is_valid():
        try: 
          form.save()
          return HttpResponseRedirect('/clanovi/izmenjeno/')
        except: 
          return HttpResponseRedirect('/greska/')      
    else:
      form = UserChangeForm(instance=clan_za_edit)
    try:
      podaci = User.objects.get(username=request.user.get_username())
    except:
      return HttpResponseRedirect('/greska/')      
    return render_to_response('profil/clan_edit.html', {'podaci':podaci , 'form':form }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/greska/')

@login_required
def profil_delete(request):
  try:
    clan_za_edit = User.objects.get(username=request.user.get_username())
  except:
    return HttpResponseRedirect('/404/')
  if request.method == 'POST':
    form = UserChangeForm(request.POST, instance=clan_za_edit)
    if form.is_valid():
      try: 
        form.save()
        return HttpResponseRedirect('/clanovi/obrisano/')
      except: 
        return HttpResponseRedirect('/greska/')      
  else:
    form = UserChangeForm(instance=clan_za_edit)
  return render_to_response('profil/clan_delete_potvrda.html', {'form':form }, context_instance=RequestContext(request))

@user_passes_test(korisnik_edit, login_url="/profil/login/")
def clan_prikaz_edit(request, clan_id):
  if request.user.is_authenticated():
    try:
      clan_za_edit = User.objects.get(pk=clan_id)
    except:
      return HttpResponseRedirect('/404/')
    if request.method == 'POST':
      form = UserChangeForm(request.POST, instance=clan_za_edit)
      if form.is_valid():
        try: 
          form.save()
          return HttpResponseRedirect('/clanovi/izmenjeno/')
        except: 
          return HttpResponseRedirect('/greska/')      
    else:
      form = UserChangeForm(instance=clan_za_edit)
    try:
      podaci = User.objects.get(id=clan_id)
    except:
      return HttpResponseRedirect('/greska/')      
    return render_to_response('profil/clan_edit.html', {'podaci':podaci , 'form':form }, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/greska/')

@user_passes_test(korisnik_edit, login_url="/profil/login/")
def clan_delete(request, clan_id):
  try:
    clan_za_edit = User.objects.get(pk=clan_id)
  except:
    return HttpResponseRedirect('/404/')
  if request.method == 'POST':
    form = UserChangeForm(request.POST, instance=clan_za_edit)
    if form.is_valid():
      try: 
        form.save()
        return HttpResponseRedirect('/clanovi/obrisano/')
      except: 
        return HttpResponseRedirect('/greska/')      
  else:
    form = UserChangeForm(instance=clan_za_edit)
  return render_to_response('profil/clan_delete_potvrda.html', {'form':form }, context_instance=RequestContext(request))
# =================================== END CLAN ===================================

def home(request):
  podaci = Projekti.objects.all().order_by('id')
  return render_to_response('projekat/lista_projekata.html', {'Projekti' : podaci}, context_instance=RequestContext(request))

# =================================== SASTANAK ===================================
def sastanak(request, sastanak_id):
  try: 
    podaci = Sastanci.objects.get(id=sastanak_id)
  except:
    return HttpResponseRedirect('/404/')
  return render_to_response('sastanak/sastanak.html', {'podaci':podaci}, context_instance=RequestContext(request))

@login_required
def sastanak_add(request):
    if request.method == 'POST':
        form = DodavanjeSastanka(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/sastanak/upisano")
    else:
        form = DodavanjeSastanka()
    return render_to_response('sastanak/sastanak_dodaj.html', {'form': form}, context_instance=RequestContext(request))

@user_passes_test(korisnik_edit, login_url="/profil/login/")
def sastanak_edit(request, sastanak_id):
  try: 
    sastanak_za_edit = Sastanci.objects.get(pk=sastanak_id)
  except:
    return HttpResponseRedirect('/404/')
  if request.method == 'POST':
    form = DodavanjeSastanka(request.POST, instance=sastanak_za_edit)
    if form.is_valid():
      try: 
        form.save()
        return HttpResponseRedirect('/sastanak/upisano/')
      except: 
        return HttpResponseRedirect('/greska/')
  else:
    form = DodavanjeSastanka(instance=sastanak_za_edit)
  try:
    podaci = Sastanci.objects.get(id=sastanak_id)
  except:
    return HttpResponseRedirect('/greska/')
  return render_to_response('sastanak/sastanak_edit.html', {'podaci':podaci , 'form':form}, context_instance=RequestContext(request))

@user_passes_test(korisnik_edit, login_url="/profil/login/")
def sastanak_delete(request, sastanak_id):
  try:
    sastanak_za_delete = Sastanci.objects.get(pk=sastanak_id)
  except:
    return HttpResponseRedirect('/404/')
  try: 
    sastanak_za_delete.delete()
    return HttpResponseRedirect('/sastanak/obrisano/')
  except:
    return HttpResponseRedirect('/greska/')
# =================================== END SASTANAK ===================================

def pretraga(request):
  greska_duga = False
  greska_nema = False
  if 'q' in request.GET:
    q = request.GET['q']
  if not q:
    greska_nema = True
    return render_to_response('pretraga/pretraga-forma.html', {'greska_nema': greska_nema}, context_instance=RequestContext(request))
  if len(q) > 30:
    greska_duga = True
    return render_to_response('pretraga/pretraga-forma.html', {'greska_duga': greska_duga}, context_instance=RequestContext(request))
  else:
    projekti = Projekti.objects.filter(naziv__icontains=q) or Projekti.objects.filter(opis__icontains=q) or Projekti.objects.filter(sala__icontains=q)
    return render_to_response('pretraga/rezultati_pretrage.html', {'projekti':projekti, 'query':q}, context_instance=RequestContext(request))
  return render_to_response('pretraga-forma.html', {'greska': greska }, context_instance=RequestContext(request))
  
def izmeni_foto(request):
  if request.user.is_authenticated():
    
    clan_za_edit = User.objects.get(username=request.user.get_username())
    try:
      profil_za_edit = Profil.objects.get(korisnik_id=clan_za_edit.id)
    except:
      return HttpResponseRedirect('/profil/fotografija/nema/')
    form = DodajProfilModel(request.POST, request.FILES, instance=profil_za_edit)
    if form.is_valid():
      try:
        form.save()
        return HttpResponseRedirect('/profil/fotografija/dodato/')
      except:
        greska = 'Greska!'
        return render_to_response('profil/dodaj_sliku.html', {'form':form, 'greska':greska}, context_instance=RequestContext(request))
    else:
      form = DodajProfilModel(instance=profil_za_edit)
      return render_to_response('profil/dodaj_sliku.html', {'form':form }, context_instance=RequestContext(request))
    return render_to_response('profil/dodaj_sliku.html', {'form':form}, context_instance=RequestContext(request))
  
  else:
    return HttpResponseRedirect('/profil/login/')
  
def dodaj_foto(request):
  if request.user.is_authenticated():
    form = DodajProfilModel(request.POST, request.FILES) 
    if form.is_valid():
      try:
        form.save()
        return HttpResponseRedirect('/profil/fotografija/dodato/')
      except:
        greska2 = 'Greska!'
        return render_to_response('profil/dodaj_sliku.html', {'form':form, 'greska2':greska2}, context_instance=RequestContext(request))
    else:
      form = DodajProfilModel()
      return render_to_response('profil/dodaj_sliku.html', {'form':form }, context_instance=RequestContext(request))
    return render_to_response('profil/dodaj_sliku.html', {'form':form}, context_instance=RequestContext(request))
  else:
    return HttpResponseRedirect('/profil/login/')