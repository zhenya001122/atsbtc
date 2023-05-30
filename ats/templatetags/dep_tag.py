from django import template
from ats.models import *


register = template.Library()

@register.simple_tag(name='getdep')
def get_department():
    return Department.objects.all()
