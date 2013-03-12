from django.db import models
from django.contrib.auth.models import User
# Create your models here.
  
class Projekti(models.Model):
  naziv = models.CharField(max_length = 150)
  koordinator = models.ForeignKey(User, related_name='projekti_koordinator')
  opis = models.TextField()
  datum_pocetak = models.DateField()
  datum_kraj = models.DateField()
  sala = models.CharField(max_length = 10)
  ukljuceni_clanovi = models.ManyToManyField(User, related_name='projekti_clanovi')
  
  def __unicode__(self):
        return "%s" % (self.naziv)
  
class Sastanci(models.Model):
  projekat = models.ForeignKey(Projekti, related_name='sastanci_projekat_izbor')
  naziv = models.CharField(max_length = 150)
  datum_odrzavanja = models.DateField()
  vrijeme_odrzavanja = models.TimeField()
  opis = models.TextField()
  prisutni_clanovi = models.ManyToManyField(User, related_name='sastanci_prisutni') 
  
class Profil(models.Model):
  korisnik = models.ForeignKey(User, related_name='profil_korisnik')
  slika = models.ImageField(upload_to='aplikacija/static/uploads/')
  
class UserPrikazImena(User):
    class Meta:
        proxy = True
    
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    def __get_id__(self):
        return "%s" % (self.id)