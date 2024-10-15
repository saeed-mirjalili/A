from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from .forms import UserLoginForm, ArticleFindForm
from django.contrib import messages
from home.models import Article

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'user registered successfully', 'success')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
                return redirect('profile')
            else:
                messages.error(request, 'username or password is wrong', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form':form})


def user_logout(request):
    logout(request)
    messages.success(request, 'you have successfully logged out', 'success')
    return redirect('home')


def user_article(request):
    form = ArticleFindForm()
    articles = Article.objects.filter(owner__id=request.user.id)
    text = 'your articles' 
    if not articles.exists():
        messages.warning(request, "you don't have any article yet")
        return redirect('home')
    return render(request, 'home.html', {'articles':articles, 'text':text, 'form':form })