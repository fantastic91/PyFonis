from django.db import models

# Create your models here.

class Clan(models.Model):
  ime = models.CharField(max_length = 40)
  prezime = models.CharField(max_length = 40)
  email = models.EmailField()

  def __unicode__(self):
    return "%s %s" % (self.ime, self.prezime)
    
  
class Projekti(models.Model):
  naziv = models.CharField(max_length = 150)
  koordinator = models.ForeignKey(Clan, related_name='projekti_koordinator')
  opis = models.TextField()
  datum_pocetak = models.DateTimeField()
  datum_kraj = models.DateTimeField()
  sala = models.CharField(max_length = 10)
  ukljuceni_clanovi = models.ManyToManyField(Clan, related_name='projekti_clanovi')