from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView

from ats.forms import AddCrossForm, AddAtsForm, AddAreaForm, AddCableForm, AddNoteForm
from ats.models import Department, Area, Ats, Cable, Cross


def index(request):
    if request.user.is_authenticated:
        context = {
            'title': 'МЛТЦ',
        }
        return render(request, 'ats/index.html', context=context)
    else:
        return redirect('login')


# @login_required #проверка авторизации
def area(request, dep_slug):
    """Возвращает список подразделений и районов по отдельному подразделению"""
    if request.user.is_authenticated:
        dep = Department.objects.get(slug=dep_slug)
        list_area = dep.areas.all()
        context = {
            'dep': dep,
            'list_area': list_area,
            'title': 'Список районов'
        }
        return render(request, 'ats/area.html', context=context)
    else:
        return redirect('login')


def add_area(request, dep_slug):
    """Добавляет район обслуживания"""
    if request.user.is_authenticated:
        dep = Department.objects.get(slug=dep_slug)
        if request.method == 'POST':
            form_area = AddAreaForm(request.POST)
            if form_area.is_valid():
                form_area.save()
                return redirect(f'/area/{dep_slug}/')
        else:
            form_area = AddAreaForm(initial={'department': dep})

        context = {
            'dep': dep,
            'form_area': form_area,
        }
        return render(request, 'ats/add_area.html', context=context)
    else:
        return redirect('login')


def ats(request, area_slug):#вернуть список районов подразделения
    """Возвращает список обслуживаемых АТС района"""
    if request.user.is_authenticated:
        ar = Area.objects.get(slug=area_slug)
        list_ats = Ats.objects.filter(area__name=ar.name)
        paginator = Paginator(list_ats, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'ar': ar,
            'list_ats': list_ats,
            'title': 'Список АТС',
            'page_obj': page_obj
        }
        return render(request, 'ats/ats_lst.html', context=context)
    else:
        return redirect('login')


def add_ats(request, area_slug):
    if request.user.is_authenticated:
        ar = Area.objects.get(slug=area_slug)
        if request.method == 'POST':
            form_ats = AddAtsForm(request.POST)
            if form_ats.is_valid():
                form_ats.save()
                return redirect(f'/ats/{area_slug}')
        else:
            form_ats = AddAtsForm(initial={'area': ar})
        context = {
            'ar': ar,
            'form_ats': form_ats,
        }
        return render(request, 'ats/add_ats.html', context=context)
    else:
        return redirect('login')


class AtsUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление: обновления АТС
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Ats
    template_name = 'ats/edit_ats.html'
    context_object_name = 'ats'
    fields = ['name', 'area']

    def get_object(self, queryset=None):
        return Ats.objects.get(slug=self.kwargs.get("ats_slug"))


def delete_ats(request, ats_slug):
    if request.user.is_authenticated:
        ats_obj = Ats.objects.get(slug=ats_slug)
        area_obj = Ats.objects.get(slug=ats_slug).area
        if request.method == 'POST':
            try:
                ats_obj.delete()
                return redirect(f'/ats/{area_obj.slug}')
            except Ats.DoesNotExist:
                return HttpResponseNotFound("<h2>АТС не найдена</h2>")
        context = {
            'ats': ats_obj,
            'area': area_obj
        }
        return render(request, 'ats/delete_ats.html', context=context)
    else:
        return redirect('login')


def ats_room(request, ats_slug):
    """Возвращает данные по АТС и список АТС, обслуживаемых подразделением"""
    if request.user.is_authenticated:
        ar = Ats.objects.get(slug=ats_slug).area
        list_ats = Ats.objects.filter(area__name=ar.name)
        at = Ats.objects.get(slug=ats_slug)
        list_cable = Cable.objects.filter(ats__name=at.name)
        list_cross = Cross.objects.filter(ats__name=at.name)
        paginator = Paginator(list_ats, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if request.method == 'POST':
            form_cable = AddCableForm(list_cross, request.POST)
            form_cross = AddCrossForm(request.POST, request.FILES)
            form_note = AddNoteForm(list_cross, list_cable, request.POST)
            if form_cable.is_valid():
                form_cable.save()
                return redirect(request.path)
            elif form_cross.is_valid():
                form_cross.save()
                return redirect(request.path)
            elif form_note.is_valid():
                form_note.save()
                return redirect(request.path)
        else:
            form_cable = AddCableForm(list_cross, initial={'ats': at})
            form_cross = AddCrossForm(initial={'ats': at})
            form_note = AddNoteForm(list_cross, list_cable)

        context = {
            'form_cable': form_cable,
            'form_cross': form_cross,
            'form_note': form_note,
            'ar': ar,
            'list_ats': list_ats,
            'at': at,
            'list_cable': list_cable,
            'list_cross': list_cross,
            'page_obj': page_obj
        }
        return render(request, 'ats/ats_room.html', context=context)
    else:
        return redirect('login')


class CableUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление: обновления КЛС
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Cable
    template_name = 'ats/edit_cable.html'
    context_object_name = 'cable'
    fields = ['sl', 'direction', 'tag', 'grounding', 'cross', 'ats']

    def get_object(self, queryset=None):
        return Cable.objects.get(slug=self.kwargs.get("cable_slug"))


class CableDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Cable
    template_name = 'ats/delete_cable.html'
    context_object_name = 'cable'
    success_url = reverse_lazy('home')#перенаправить на ats_room/ats_slug/ ,
                    # как извлечь и передать ats_slug в reverse_lazy("ats_room")?

    def get_object(self, queryset=None):
        return Cable.objects.get(slug=self.kwargs.get("cable_slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ats'] = Cable.objects.get(slug=self.object.slug).ats
        return context


class CrossUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление: обновления кросса
    """
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Cross
    template_name = 'ats/edit_cross.html'
    context_object_name = 'cross'
    fields = ['number', 'tag', 'photo_cross', 'photo_insert', 'ats']

    def get_object(self, queryset=None):
        return Cross.objects.get(slug=self.kwargs.get("cross_slug"))

def delete_cross(request, cross_slug):
    if request.user.is_authenticated:
        cross_obj = Cross.objects.get(slug=cross_slug)
        ats_obj = Cross.objects.get(slug=cross_slug).ats
        if request.method == 'POST':
            try:
                cross_obj.delete()
                return redirect(f'/ats_room/{ats_obj.slug}')
            except Ats.DoesNotExist:
                return HttpResponseNotFound("<h2>Кросс не найден</h2>")
        context = {
            'ats': ats_obj,
            'cross': cross_obj
        }
        return render(request, 'ats/delete_cross.html', context=context)
    else:
        return redirect('login')
