from django.contrib import admin
from django.forms import CheckboxSelectMultiple

from django.db import models
from ats.models import Department, Area, Ats, Cable, Cross, Note


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)} #автозаполнение поля slug при вводе поля name в админке



@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


@admin.register(Ats)
class AtsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Cable)
class CableAdmin(admin.ModelAdmin):
    list_display = ('sl', 'direction', 'tag', 'grounding', 'passport', 'time_create', 'time_update')
    list_filter = ('tag', 'grounding')
    list_display_links = ('sl', 'direction',)
    list_editable = ('grounding',)
    search_fields = ('sl', 'direction')
    prepopulated_fields = {"slug": ("direction",)}


@admin.register(Cross)
class CrossAdmin(admin.ModelAdmin):
    list_display = ('number', 'ats', 'tag', 'photo_cross', 'photo_insert', 'time_create', 'time_update')
    list_filter = ('tag',)
    list_editable = ('tag',)
    prepopulated_fields = {"slug": ("number",)}


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('description', 'cable', 'cross')
    search_fields = ('description',)
