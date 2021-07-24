from django.contrib import admin as dj_admin
from django_neomodel import admin as neo_admin

from .models import Movie, Person

class MovieAdmin(dj_admin.ModelAdmin):
    list_display = ("title","uuid")
neo_admin.register(Movie, MovieAdmin)


class PersonAdmin(dj_admin.ModelAdmin):
    list_display = ("name","uuid")
neo_admin.register(Person, PersonAdmin)