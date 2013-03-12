from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.conf.urls.defaults import *
from django.contrib import admin
#from aplikacija.views import provjera_logina
from aplikacija.models import Projekti
from django.contrib.auth.views import login, logout 
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:    
    url(r'^$', 'aplikacija.views.home', name='home'),
    
    url(r'^projekti/$', 'aplikacija.views.home'),
    url(r'^projekti/prikaz/(?P<projekat_id>\d+)/$', 'aplikacija.views.projekat'),
    url(r'^projekti/prikaz/(?P<projekat_id>\d+)/edit/$', 'aplikacija.views.projekat_edit'),
    url(r'^projekti/prikaz/(?P<projekat_id>\d+)/delete/$', 'aplikacija.views.projekat_delete'),
    url(r'^projekti/novi/$', 'aplikacija.views.projekat_add'),
    url(r'^projekti/upisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'projekat/projekat_upisano.html' }),
    url(r'^projekti/obrisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'projekat/projekat_obrisano.html' }),
    
    url(r'^clanovi/$', 'aplikacija.views.clan'),
    url(r'^clanovi/prikaz/(?P<clan_id>\d+)/$', 'aplikacija.views.clan_prikaz'),
    url(r'^clanovi/prikaz/(?P<clan_id>\d+)/edit/$', 'aplikacija.views.clan_prikaz_edit'),
    url(r'^clanovi/prikaz/(?P<clan_id>\d+)/delete/$', 'aplikacija.views.clan_delete'),  
    url(r'^clanovi/izmenjeno/$', 'aplikacija.views.opsti_response', { 'template_name' : 'profil/clan_izmenjeno.html' }), 
    url(r'^clanovi/obrisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'profil/clan_obrisano.html' }), 
    
    url(r'^pretraga/$', 'aplikacija.views.pretraga'),
    url(r'^greska/$', 'aplikacija.views.opsti_response', { 'template_name' : 'neupisano.html' }),  
    url(r'^404/$', 'aplikacija.views.opsti_response', { 'template_name' : '404.html' }),       
   
    url(r'^sastanak/$', 'aplikacija.views.sastanak'),
    url(r'^sastanak/novi/$', 'aplikacija.views.sastanak_add'),
    url(r'^sastanak/upisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'sastanak/sastanak_upisano.html' }),
    url(r'^sastanak/(?P<sastanak_id>\d+)/$', 'aplikacija.views.sastanak'),
    url(r'^sastanak/(?P<sastanak_id>\d+)/edit/$', 'aplikacija.views.sastanak_edit'),
    url(r'^sastanak/(?P<sastanak_id>\d+)/delete/$', 'aplikacija.views.sastanak_delete'),
    url(r'^sastanak/obrisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'sastanak/sastanak_obrisano.html' }), 
        
    url(r'^profil/registracija/$',  'aplikacija.views.registracija'),
    url(r'^profil/login/$',  login, { 'template_name' : 'profil/login.html' }),
    url(r'^accounts/login/$',  login, { 'template_name' : 'profil/login.html' }),
    url(r'^profil/logout/$', logout, { 'template_name' : 'profil/logout.html', }),
    url(r'^profil/lozinka/promena/$', 'django.contrib.auth.views.password_change', { 'template_name': 'profil/promena_pass.html'}),
    url(r'^profil/lozinka/uspesno/$', 'django.contrib.auth.views.password_change_done', { 'template_name': 'profil/uspesna_promena_pass.html'}),
    url(r'^profil/kreiran/$', 'aplikacija.views.opsti_response', { 'template_name' : 'profil/kreiran.html' }),
    url(r'^profil/fotografija/$', 'aplikacija.views.izmeni_foto'),
    url(r'^profil/fotografija/dodaj/$', 'aplikacija.views.dodaj_foto'),
    url(r'^profil/fotografija/dodato/$', 'aplikacija.views.opsti_response', { 'template_name' : 'profil/fotografija_upisano.html' }),
    url(r'^profil/fotografija/nema/$', 'aplikacija.views.opsti_response', { 'template_name' : 'profil/fotografija_nema.html' }),
    url(r'^profil/$', 'aplikacija.views.profil'),
    url(r'^profil/edit/$', 'aplikacija.views.profil_edit'),
    url(r'^profil/delete/$', 'aplikacija.views.profil_delete'),
   
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
