from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('detail/<int:article_id>', views.detail, name='detail'),
    path('remove/<int:article_id>', views.remove, name='remove'),
    path('add/<int:article_id>', views.add, name='add'),
    path('upload/', views.upload, name='upload'),
    path('review/<int:article_id>', views.review, name='review'),
]