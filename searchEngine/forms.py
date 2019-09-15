from django import forms
from . import models

class searchForm(forms.ModelForm):
    class Meta:
        model = models.SearchBox
        fields = ['search',]

class LoginForm(forms.ModelForm):
    class Meta:
        model = models.LoginData
        fields = "__all__"  


class OtpForm(forms.ModelForm):
    class Meta:
        model = models.OtpData
        fields = "__all__"  
