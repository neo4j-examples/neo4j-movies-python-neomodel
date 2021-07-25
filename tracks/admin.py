from django.contrib import admin as dj_admin
from django_neomodel import admin as neo_admin

from .models import TrackGroup, Tag, Track, RUser

class RUserAdmin(dj_admin.ModelAdmin):
    list_display = ("uuid","uuid")
neo_admin.register(RUser, RUserAdmin)

class TrackGroupAdmin(dj_admin.ModelAdmin):
    list_display = ("title","type","uuid")
neo_admin.register(TrackGroup, TrackGroupAdmin)

class TagAdmin(dj_admin.ModelAdmin):
    list_display = ("name","uuid")
neo_admin.register(Tag, TagAdmin)

class TrackAdmin(dj_admin.ModelAdmin):
    list_display = ("title","uuid")
neo_admin.register(Track, TrackAdmin)