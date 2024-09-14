from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleCreateForm
from django.contrib import messages


def home(request):
    person = {'name':'saeed','age':'22','gender':'male'}
    articles = Article.objects.all()

    return render(request, 'home.html', {'person':person,'articles':articles})


def detail(request, article_id):
    article = Article.objects.get(id = article_id)
    
    return render(request , 'detail.html' , {'article':article})


def delete(request, article_id):
    Article.objects.get(id=article_id).delete()
    messages.success(request, 'Article deleted successfully', 'success')

    return redirect('home')


def create(request):
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Article.objects.create(title=cd['title'], body=cd['body'], created=cd['created'])
            messages.success(request, 'Article create successfully', 'success')

            return redirect('home')
    else:
        form = ArticleCreateForm()
    return render(request, 'create.html', {'form':form})

