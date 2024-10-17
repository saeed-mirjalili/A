from django.shortcuts import render

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Article, Like

def toggle(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like, created = Like.objects.get_or_create(user=request.user, article=article)

    if created:
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        like.delete()
        return redirect(request.META.get('HTTP_REFERER', 'home'))

