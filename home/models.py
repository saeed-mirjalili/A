from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    # body = models.TextField()
    pdf = models.FileField(upload_to='%Y/%m/%d/')
    # created = models.DateTimeField()
    
