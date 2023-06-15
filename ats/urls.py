from django.urls import path

from .views import index, area, ats, ats_room, add_area, add_ats, delete_ats, AtsUpdateView, CableUpdateView, \
    CableDeleteView

urlpatterns = [
    path('', index, name='home'),
    path('ats/<slug:area_slug>/', ats, name='ats'),
    path('add_ats/<slug:area_slug>/', add_ats, name='add_ats'),
    path('add_area/<slug:dep_slug>/', add_area, name='add_area'),
    path('edit_ats/<slug:ats_slug>/', AtsUpdateView.as_view(), name='edit_ats'),
    path('delete_ats/<slug:ats_slug>/', delete_ats, name='delete_ats'),
    path('area/<slug:dep_slug>/', area, name='area'),
    path('ats_room/<slug:ats_slug>/', ats_room, name='ats_room'),
    path('edit_cable/<slug:cable_slug>/', CableUpdateView.as_view(), name='edit_cable'),
    path('delete_cable/<slug:cable_slug>', CableDeleteView.as_view(), name='delete_cable')
]

