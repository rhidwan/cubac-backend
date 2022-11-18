from django import forms
from .models import *

from django import forms

class CallForApplicationForm(forms.ModelForm):
    class Meta:
        model = CallForApplication
        exclude = ('updated_on', 'created_on')
