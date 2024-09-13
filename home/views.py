from django.shortcuts import render
from .models import Article

def home(request):
    person = {'name':'saeed','age':'22','gender':'male'}
    articles = Article.objects.all()

    return render(request, 'home.html', {'person':person,'articles':articles})


def detail(request, article_id):
    article = Article.objects.get(id = article_id)
    
    return render(request , 'detail.html' , {'article':article})
