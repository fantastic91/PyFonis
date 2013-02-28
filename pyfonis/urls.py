from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.conf.urls.defaults import *
from django.contrib import admin
from aplikacija.views import provjera_logina
from aplikacija.models import Projekti, Clan
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:    
    url(r'^$', 'aplikacija.views.home', name='home'),
    
    url(r'^projekti/$', 'aplikacija.views.home'),
    url(r'^projekti/prikaz/(?P<projekat_id>\d+)/$', 'aplikacija.views.projekat'),
    url(r'^projekti/prikaz/(?P<projekat_id>\d+)/edit/$', 'aplikacija.views.projekat_edit'),
    url(r'^projekti/prikaz/(?P<projekat_id>\d+)/delete/$', 'aplikacija.views.projekat_delete'),
    url(r'^projekti/novi/$', 'aplikacija.views.upis'),
    url(r'^projekti/upisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'projekat_upisano.html' }),
    url(r'^projekti/obrisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'projekat_obrisano.html' }),
    
    url(r'^clanovi/$', 'aplikacija.views.clan'),
    url(r'^clanovi/prikaz/(?P<clan_id>\d+)/$', 'aplikacija.views.clan_prikaz'),
    url(r'^clanovi/prikaz/(?P<clan_id>\d+)/edit/$', 'aplikacija.views.clan_prikaz_edit'),
    url(r'^clanovi/prikaz/(?P<clan_id>\d+)/delete/$', 'aplikacija.views.clan_delete'),  
    url(r'^clanovi/novi/$', 'aplikacija.views.clan_dodaj'),
    url(r'^clanovi/upisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'clan_upisano.html' }),
    url(r'^clanovi/obrisano/$', 'aplikacija.views.opsti_response', { 'template_name' : 'clan_obrisano.html' }), 
    
    url(r'^pretraga/$', 'aplikacija.views.pretraga'),
    url(r'^greska/$', 'aplikacija.views.opsti_response', { 'template_name' : 'neupisano.html' }),  
    url(r'^404/$', 'aplikacija.views.opsti_response', { 'template_name' : '404.html' }),       
    url(r'^accounts/login/$', 'aplikacija.views.accounts_login'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
