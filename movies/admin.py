from django.contrib import admin as dj_admin
from django_neomodel import admin as neo_admin

from .models import Movie

class MovieAdmin(dj_admin.ModelAdmin):
    list_display = ("title",)
neo_admin.register(Movie, MovieAdmin)


# Register your models here.
