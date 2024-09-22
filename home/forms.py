from django import forms
from .models import Article


class ArticleUploadForm(forms.Form):
    title = forms.CharField()
    pdf = forms.FileField()


class ArticleReviewForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body']

class ArticleSearchForm(forms.Form):
    word = forms.CharField()