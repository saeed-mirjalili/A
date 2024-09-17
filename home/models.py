from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    pdf = models.FileField(upload_to='%Y/%m/%d/')
    created = models.DateTimeField(auto_now_add=True)
    
    # def __str__(self):
    #     return self.body[:50]