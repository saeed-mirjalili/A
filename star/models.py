from django.db import models
from django.contrib.auth.models import User
from home.models import Article

class Like(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    article = models.ForeignKey(Article ,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
