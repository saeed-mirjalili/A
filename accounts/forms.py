from django import forms

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.FileField()