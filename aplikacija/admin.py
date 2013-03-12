from django.contrib import admin
from aplikacija.models import Projekti, Profil

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

admin.site.register(Projekti)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'profil'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfilInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)