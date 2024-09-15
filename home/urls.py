from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('detail/<int:article_id>', views.detail, name='detail'),
    path('delete/<int:article_id>', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('readpdf/<str:pdf_file>/<str:current_word>', views.find_next_word_in_pdf)
]