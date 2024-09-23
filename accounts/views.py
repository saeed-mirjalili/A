from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def user_register(request):
    user = User.objects.create_user('johna','john@infoa.com','123')
    user.save()
    return redirect('home')
