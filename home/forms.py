from django import forms
from .models import Article


class ArticleUploadForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    pdf = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))


class ArticleReviewForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'lang']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'lang': forms.HiddenInput(),
        }


class ArticleSearchForm(forms.Form):
    word = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


class ArticleFindForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Word search in summary of articles'}))