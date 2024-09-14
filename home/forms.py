from django import forms

class ArticleCreateForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField()
    created = forms.DateTimeField()