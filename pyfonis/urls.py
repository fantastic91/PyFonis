from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from aplikacija.views import provjera_logina
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/login/$', 'aplikacija.views.accounts_login'),
    url(r'^$', 'aplikacija.views.home', name='home'),
    #url(r'^pyfonis/', include('pyfonis.aplikacija.foo.urls')),
    url(r'^articles/(\d{4})/(\d{2})/(\d{2})/$', 'aplikacija.views.day_archive'),
    url(r'^upis/$', 'aplikacija.views.upis', name='upis'),
    url(r'^clan/dodaj/$', 'aplikacija.views.clan_dodaj'),
    url(r'^lista/$', 'aplikacija.views.home'),
    url(r'^clan/$', 'aplikacija.views.clan'),
    url(r'^pretraga-forma/$', 'aplikacija.views.pretraga_forma'),
    url(r'^pretraga/$', 'aplikacija.views.pretraga'),
    url(r'^upis/upisano/$', 'aplikacija.views.upis_upisano'),
    url(r'^clan/upisano/$', 'aplikacija.views.clan_upisano'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)