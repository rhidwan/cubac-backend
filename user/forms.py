from django import forms
from .models import User

from django import forms
from django.core.exceptions import ValidationError
 
 
class ClientUserCreationForm(forms.Form):
    mobile_no = forms.CharField(label='Enter Mobile No', min_length=8, max_length=20)
    name = forms.CharField(label="Name", max_length=200)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    designation = forms.CharField(label="Designation", max_length=200, required=False)
    department = forms.CharField(label="Department", max_length=200, required=False)
 
    def clean_mobile_no(self):
        mobile_no = self.cleaned_data['mobile_no'].lower()
        r = User.objects.filter(mobile_no=mobile_no)
        if r.count():
            raise  ValidationError("Mobile No already exists")
        return mobile_no
 
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2
 
    def save(self, commit=True):
        user = User.objects.create_user(
            mobile_no = self.cleaned_data['mobile_no'],
            name= self.cleaned_data['name'],
            password=self.cleaned_data['password1'],
            user_type=0,
            designation=self.cleaned_data['designation'],
            department=self.cleaned_data['department']
        )
        return user

