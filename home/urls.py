from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home),
    path('detail/<int:article_id>', views.detail, name='detail')
]