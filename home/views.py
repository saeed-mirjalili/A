import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleReviewForm
from .forms import ArticleUploadForm
from django.contrib import messages
from PyPDF2 import PdfReader


def home(request):
    person = {'name':'saeed','age':'22','gender':'male'}
    articles = Article.objects.all()

    return render(request, 'home.html', {'person':person,'articles':articles})




def detail(request, article_id):  
    article = Article.objects.get(id=article_id)  
    pdf_path = article.pdf.path 
    current_words = ['عنوان مقاله', 'موضوع','Title','title']  # لیست کلمات کلیدی
    
    next_sentences = {}  # دیکشنری برای نگهداری جملات بعدی برای هر کلمه کلیدی
    
    if not os.path.exists(pdf_path):
        messages.error(request, f"File not found: {pdf_path}")
        return render(request, 'detail.html', {'article': article, 'next_sentences': next_sentences})

    with open(pdf_path, 'rb') as file:   
        pdf_reader = PdfReader(file)           
        
        for page_num in range(len(pdf_reader.pages)):   
            page = pdf_reader.pages[page_num]   
            text = page.extract_text()   
              
            for current_word in current_words:  # جستجو برای هر کلمه کلیدی
                if current_word in text:   
                    sentences = text.split('\n')  # فرض بر این است که جملات با اینتر جدا شده‌اند  
                    
                    for i, sentence in enumerate(sentences):  
                        if current_word in sentence:  
                            # اگر جمله حاوی current_word پیدا شد، جمله بعدی را نمایش می‌دهیم  
                            if i + 1 < len(sentences):  
                                next_sentences[current_word] = sentences[i + 1]  # ذخیره جمله بعدی
                            else:  
                                messages.success(request, f"No sentence found after '{current_word}'.", 'danger')  
                            break  # پس از پیدا کردن جمله بعدی از حلقه خارج می‌شویم 
                    
            if current_word in next_sentences:  # اگر برای این کلمه جمله بعدی پیدا شد، از حلقه خارج می‌شویم
                break 

    # بررسی اینکه آیا هیچ کلمه‌ای پیدا نشده است
    if not next_sentences:   
        messages.success(request, f"None of the words {', '.join(current_words)} found in the PDF", 'danger')   

    # ارسال داده‌ها به قالب 
    return render(request, 'detail.html', {'article': article, 'next_sentences': next_sentences})




def delete(request, article_id):
    Article.objects.get(id=article_id).delete()
    messages.success(request, 'Article deleted successfully', 'success')

    return redirect('home')


def upload(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article(title=form.cleaned_data['title'], pdf=request.FILES['pdf'])
            article.save()

            return redirect('review', article_id=article.id)
    else:
        form = ArticleUploadForm()
        return render(request, 'upload.html', {'form':form})


def review(request, article_id):
    article = Article.objects.get(id=article_id)
    if request.method == 'POST':
        form = ArticleReviewForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'your Article created successfully', 'success')

            return redirect('home')
    else:
        form = ArticleReviewForm(instance=article)
        form.initial['body'] = 'مقدار مشخص شما برای فیلد'

        return render(request, 'review.html', {'form':form, 'article':article})