from django import forms
from .models import *

from django import forms

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ('payment_type', 'user', 'application')
