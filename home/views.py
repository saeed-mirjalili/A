
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleReviewForm
from .forms import ArticleUploadForm
from .forms import ArticleSearchForm
from django.contrib import messages
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langdetect import detect





def home(request):
    person = {'name':'saeed','age':'22','gender':'male'}
    articles = Article.objects.all()

    return render(request, 'home.html', {'person':person,'articles':articles})


def detail(request, article_id):  
    article = Article.objects.get(id=article_id) 
    if request.method == 'POST':
        form = ArticleSearchForm(request.POST)
        if form.is_valid():
            pdf_path = article.pdf.path 
            current_word = form.cleaned_data['word'] 
            next_sentence = ''
            with open(pdf_path, 'rb') as file:  
                pdf_reader = PdfReader(file)          
                found_current_word = False  
                for page_num in range(len(pdf_reader.pages)):  
                    page = pdf_reader.pages[page_num]  
                    text = page.extract_text()  
                    if current_word in text:  
                        found_current_word = True  
                        sentences = text.split('\n') 
                        for i, sentence in enumerate(sentences): 
                            if current_word in sentence: 
                                if i + 1 < len(sentences): 
                                    next_sentence = sentences[i]+sentences[i + 1] 
                                else: 
                                    messages.success(request, "No sentence found after the title.", 'danger') 
                                break  
                        break  
                if not found_current_word:  
                    messages.success(request, f"Word '{current_word}' not found in the PDF", 'danger')  
        
            return render(request, 'detail.html', {'article': article, 'next_sentences': next_sentence, 'form':form})
    else:
        form = ArticleSearchForm()

        return render(request, 'detail.html', {'article': article, 'form':form})


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
        with open(article.pdf.path, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        language = detect(text)

        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 3)  # تعداد جملات خلاصه
        form.initial['body'] = ' '.join(str(sentence) for sentence in summary)
        form.initial['lang'] = language

        return render(request, 'review.html', {'form':form, 'lang': language})