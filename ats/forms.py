from django import forms
from .models import *


class AddAreaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].empty_label = "Выберите подразделение"
    class Meta:
        model = Area
        fields = ['name', 'department']


class AddAtsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['area'].empty_label = "Выберите район"
    class Meta:
        model = Ats
        fields = ['name', 'area']


class AddCableForm(forms.ModelForm):
    def __init__(self, list_cross, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cross'].empty_label = "Выберите кросс"
        self.fields['cross'].queryset = list_cross
        self.fields['ats'].empty_label = "Выберите АТС"
    class Meta:
        model = Cable
        fields = ['sl', 'direction', 'tag', 'grounding', 'passport', 'cross', 'ats']


class AddCrossForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ats'].empty_label = "Выберите АТС"
    class Meta:
        model = Cross
        fields = ['number', 'tag', 'photo_cross', 'photo_insert', 'ats']


class AddNoteForm(forms.ModelForm):
    def __init__(self, list_cross, list_cable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cable'].empty_label = "Выберите КЛС"
        self.fields['cable'].queryset = list_cable
        self.fields['cross'].empty_label = "Выберите кросс"
        self.fields['cross'].queryset = list_cross
    class Meta:
        model = Note
        fields = '__all__'
