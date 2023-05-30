from django.urls import path

from .views import index, area, ats, ats_room, add_area, add_ats

urlpatterns = [
    path('', index, name='home'),
    path('ats/<slug:area_slug>/', ats, name='ats'),
    path('add_ats/<slug:area_slug>/', add_ats, name='add_ats'),
    path('add_area/<slug:dep_slug>/', add_area, name='add_area'),
    path('area/<slug:dep_slug>/', area, name='area'),

    path('ats_room/<slug:ats_slug>/', ats_room, name='ats_room'),

]

