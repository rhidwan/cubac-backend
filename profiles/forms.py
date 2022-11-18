from django import forms
from .models import *

from django import forms
from django.core.exceptions import ValidationError
 
 
# class BasicInfoForms(forms.Form):
class BasicInfoForm(forms.ModelForm):

    class Meta:
        model = BasicInfo
        exclude = ('user', 'photo')


class TestScoreForm(forms.ModelForm):
    class Meta:
        model = TestScore
        exclude = ('user',)
    
class AchievementMembershipForm(forms.ModelForm):
    class Meta:
        model = AchievementMembership
        exclude = ('user',)

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ('user',)

class EducationalBackgroundForm(forms.ModelForm):
    class Meta:
        model = EducationalBackground
        exclude = ('user',)
