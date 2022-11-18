from django import forms
from .models import User
from django.core.exceptions import ValidationError
 
 
class UserRegistrationForm(forms.Form):
    GENDER_CHOICES = [(0, 'Male'), (1, 'Female'), (2, 'Other')]
    email = forms.EmailField(label='Enter email', min_length=8, max_length=50)
    full_name = forms.CharField(label="Name", max_length=200)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(label="Date Of Birth", required=False)
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES) 
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
 
 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2
 
    def save(self, commit=True):
        user = User.objects.create_user(
            email = self.cleaned_data['email'],
            full_name= self.cleaned_data['full_name'],
            password=self.cleaned_data['password1'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            gender=self.cleaned_data['gender']
        )
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('date_of_birth', 'gender', 'full_name', )
