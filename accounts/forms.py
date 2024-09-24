from django import forms

class UserRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()