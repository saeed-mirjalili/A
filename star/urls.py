from django.urls import path
from . import views

urlpatterns = [
    path('star/<int:article_id>', views.toggle, name='like'),
]