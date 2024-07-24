from django import forms
from django.contrib.auth.models import User
from . import models
from exam import models as QMODEL

class IntervieweeUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class IntervieweeForm(forms.ModelForm):
    class Meta:
        model=models.Interviewee
        fields=['address','mobile','profile_pic']

