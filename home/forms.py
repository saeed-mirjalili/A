from django import forms
from .models import Article


class ArticleUploadForm(forms.Form):
    title = forms.CharField()
    pdf = forms.FileField()


class ArticleReviewForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'lang']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lang'].widget = forms.HiddenInput()  # مخفی کردن فیلد lang

class ArticleSearchForm(forms.Form):
    word = forms.CharField()