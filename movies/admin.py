from django.contrib import admin as dj_admin
from django_neomodel import admin as neo_admin

from .models import Movie, Person

# warning! If you're using Sandbox you'll have to add uuids

class MovieAdmin(dj_admin.ModelAdmin):
    list_display = ("title","uuid")
neo_admin.register(Movie, MovieAdmin)


class PersonAdmin(dj_admin.ModelAdmin):
    list_display = ("name","uuid")
neo_admin.register(Person, PersonAdmin)