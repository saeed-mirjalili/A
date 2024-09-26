from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pdf = models.FileField(upload_to='%Y/%m/%d/')
    lang = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ManyToManyField(User, related_name='articles')

class Meta:
    unique_together = ('article', 'user')