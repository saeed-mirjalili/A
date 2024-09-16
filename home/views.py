import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleCreateForm
from django.contrib import messages
from PyPDF2 import PdfReader


def home(request):
    person = {'name':'saeed','age':'22','gender':'male'}
    articles = Article.objects.all()

    return render(request, 'home.html', {'person':person,'articles':articles})


def detail(request, article_id):
    article = Article.objects.get(id = article_id)
    
    return render(request , 'detail.html' , {'article':article})


def delete(request, article_id):
    Article.objects.get(id=article_id).delete()
    messages.success(request, 'Article deleted successfully', 'success')

    return redirect('home')


def create(request):
    if request.method == 'POST':
        form = ArticleCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Article.objects.create(title=cd['title'], body=cd['body'], created=cd['created'])
            messages.success(request, 'Article create successfully', 'success')

            return redirect('home')
    else:
        form = ArticleCreateForm()
    return render(request, 'create.html', {'form':form})



def find_next_word_in_pdf(request, pdf_file, current_word): 
    pdf_path = os.path.join(settings.BASE_DIR, 'home', 'pdf', pdf_file + '.pdf') 

    with open(pdf_path, 'rb') as file: 
        pdf_reader = PdfReader(file)         
        found_current_word = False 

        for page_num in range(len(pdf_reader.pages)): 
            page = pdf_reader.pages[page_num] 
            text = page.extract_text() 
            
            if current_word in text: 
                found_current_word = True 
                
                # تقسیم متن به جملات
                sentences = text.split('\n')  # فرض بر این است که جملات با اینتر جدا شده‌اند
                
                for i, sentence in enumerate(sentences):
                    if current_word in sentence:
                        # اگر جمله حاوی current_word پیدا شد، جمله بعدی را نمایش می‌دهیم
                        if i + 1 < len(sentences):
                            next_sentence = sentences[i + 1]
                            messages.success(request, f'Title of your article is: {next_sentence}', 'success')
                        else:
                            messages.success(request, "No sentence found after the title.", 'danger')
                        return redirect('home')
                
                # اگر کلمه در جمله‌ای پیدا نشد
                messages.success(request, f"No sentence found containing '{current_word}' on page {page_num + 1}", 'danger') 
                return redirect('home') 

        if not found_current_word: 
            messages.success(request, f"Word '{current_word}' not found in the PDF", 'danger') 
            return redirect('home')
