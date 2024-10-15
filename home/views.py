
from django.shortcuts import render, redirect
from .models import Article
from star.models import Like
from .forms import ArticleReviewForm
from .forms import ArticleUploadForm
from .forms import ArticleSearchForm, ArticleFindForm
from django.contrib import messages
from PyPDF2 import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langdetect import detect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from nltk.tokenize import word_tokenize
from django.db.models import Count
import fitz
from collections import Counter



def home(request): 
    articles = Article.objects.annotate(like_count=Count('like')).order_by('-created')
    num = articles.count()
    form = ArticleFindForm()
    if request.GET.get('search'): 
        articles = articles.filter(body__contains=request.GET['search']) 
        text = 'Search results' 
    else:
        articles = articles[:4]
        text = 'Latest articles' 

    return render(request, 'home.html', {'articles': articles, 'form': form, 'text': text, 'num':num})





def detail(request, article_id):  
    article = get_object_or_404(Article, id=article_id) 



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


def remove(request, article_id):
    article = Article.objects.get(id=article_id)
    article.owner.remove(request.user.is_authenticated)
    messages.success(request, 'an article remove from your profile successfully', 'success')

    return redirect('home')


def add(request, article_id):
    article = Article.objects.get(id=article_id)
    article.owner.add(request.user.is_authenticated)
    messages.success(request, 'an article add to your profile successfully', 'success')

    return redirect('home')

@login_required()
def upload(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article(title=form.cleaned_data['title'], pdf=request.FILES['pdf'])
            article.save()
            article.owner.add(request.user.is_authenticated)

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
        # with open(article.pdf.path, 'rb') as file:
        #     reader = PdfReader(file)
        #     text = ''
        #     if len(reader.pages) >= 3 :
        #         for page in reader.pages[1:-1]:
        #             text += page.extract_text()
        #     else:
        #         for page in reader.pages:
        #             text += page.extract_text()

        document = fitz.open(article.pdf.path)
        text = ""
        for page in document:
            text += page.get_text("text")
        cleaned_text = text.replace("\n", ".")

        language = detect(cleaned_text)
        if language == 'en':
            parser = PlaintextParser.from_string(cleaned_text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, 3)
            body = ' '.join(str(sentence) for sentence in summary)
        else:


            words = word_tokenize(cleaned_text)
            stopWord = ['!',',','.',':',';','،','؛','؟','(',')','اﯾـﻦ','ﯾﺎ','ﻣﻲ',
                        'ﺗﺎ','به','ﻫﺮ','اﺳﺖ','ﮐﺪام','آباد','آره','آری','آمد',
                        'آمده','آن','آنان','آنجا','آنطور','آنقدر','آنكه','آنها',
                        'آنچه','آنکه','آورد','آورده','آيد','آی','آیا','آیند',
                        'اتفاقا','اثرِ','احتراما','احتمالا','اخیر','اری','از',
                        'ازجمله','اساسا','است','استفاد','استفاده','اش',
                        'اشکارا','اصلا','اصولا','اعلام','اغلب','اكنون','الان',
                        'البته','البتّه','ام','اما','امروز','امروزه','امسال',
                        'امشب','امور','ان','انجام','اند','انشاالله','انصافا',
                        'انطور','انقدر','انها','انچنان','انکه','انگار','او',
                        'اول','اولا','اي','ايشان','ايم','اين','اينكه','اکثرا',
                        'اکنون','اگر','ای','ایا','اید','ایشان','ایم','این',
                        'اینجا','ایند','اینطور','اینقدر','اینها','اینچنین',
                        'اینک','اینکه','اینگونه','با','بار','بارة','باره',
                        'بارها','باز','بازهم','باش','باشد','باشم','باشند',
                        'باشيم','باشی','باشید','باشیم','بالا','بالاخره','بالایِ',
                        'بالطبع','بايد','باید','بتوان','بتواند','بتوانی',
                        'بتوانیم','بخش','بخشی','بخواه','بخواهد','بخواهم',
                        'بخواهند','بخواهی','بخواهید','بخواهیم','بد','بدون',
                        'بر','برابر','برابرِ','براحتی','براساس','براستی',
                        'براي','برای','برایِ','برخوردار','برخي','برخی','برداري',
                        'برعکس','بروز','بزرگ','بزودی','بسا','بسيار','بسياري',
                        'بسیار','بسیاری','بطور','بعد','بعدا','بعدها','بعری',
                        'بعضا','بعضي','بلافاصله','بلكه','بله','بلکه','بلی',
                        'بنابراين','بنابراین','بندي','به','بهتر','بهترين','بود',
                        'بودم','بودن','بودند','بوده','بودی','بودید','بودیم','بویژه',
                        'بي','بيست','بيش','بيشتر','بيشتري','بين','بکن','بکند','بکنم',
                        'بکنند','بکنی','بکنید','بکنیم','بگو','بگوید','بگویم','بگویند',
                        'بگویی','بگویید','بگوییم','بگیر','بگیرد','بگیرم','بگیرند',
                        'بگیری','بگیرید','بگیریم','بی','بیا','بیاب','بیابد','بیابم',
                        'بیابند','بیابی','بیابید','بیابیم','بیاور','بیاورد','بیاورم',
                        'بیاورند','بیاوری','بیاورید','بیاوریم','بیاید','بیایم','بیایند',
                        'بیایی','بیایید','بیاییم','بیرون','بیرونِ','بیش','بیشتر','بیشتری',
                        'بین','ت','تا','تازه','تاكنون','تان','تاکنون','تحت','تر',
                        'تر  براساس','ترين','تقریبا','تلویحا','تمام','تماما','تمامي',
                        'تنها','تو','تواند','توانست','توانستم','توانستن','توانستند',
                        'توانسته','توانستی','توانستیم','توانم','توانند','توانی','توانید',
                        'توانیم','توسط','تولِ','تویِ','ثانیا','جا','جاي','جايي','جای','جدا',
                        'جديد','جدید','جريان','جریان','جز','جلوگيري','جلویِ','جمعا','جناح',
                        'جهت','حاضر','حال','حالا','حتما','حتي','حتی','حداکثر','حدودا','حدودِ',
                        'حق','خارجِ','خب','خدمات','خصوصا','خلاصه','خواست','خواستم','خواستن',
                        'خواستند','خواسته','خواستی','خواستید','خواستیم','خواهد','خواهم',
                        'خواهند','خواهيم','خواهی','خواهید','خواهیم','خوب','خود','خودت',
                        'خودتان','خودش','خودشان','خودم','خودمان','خوشبختانه','خويش','خویش',
                        'خویشتن','خیاه','خیر','خیلی','داد','دادم','دادن','دادند','داده','دادی',
                        'دادید','دادیم','دار','دارد','دارم','دارند','داريم','داری','دارید',
                        'داریم','داشت','داشتم','داشتن','داشتند','داشته','داشتی','داشتید',
                        'داشتیم','دانست','دانند','دایم','دایما','در','درباره','درمجموع','درون',
                        'دریغ','دقیقا','دنبالِ','ده','دهد','دهم','دهند','دهی','دهید','دهیم','دو',
                        'دوباره','دوم','ديده','ديروز','ديگر','ديگران','ديگري','دیر','دیروز','دیگر',
                        'دیگران','دیگری','را','راحت','راسا','راستی','راه','رسما','رسید','رفت','رفته',
                        'رو','روب','روز','روزانه','روزهاي','روي','روی','رویِ','ريزي','زمان','زمانی',
                        'زمینه','زود','زياد','زير','زيرا','زیر','زیرِ','سابق','ساخته','سازي','سالانه',
                        'سالیانه','سایر','سراسر','سرانجام','سریعا','سریِ','سعي','سمتِ','سوم','سوي',
                        'سوی','سویِ','سپس','شان','شايد','شاید','شخصا','شد','شدم','شدن','شدند','شده',
                        'شدی','شدید','شدیدا','شدیم','شش','شش  نداشته','شما','شناسي','شود','شوم','شوند',
                        'شونده','شوی','شوید','شویم','صرفا','صورت','ضدِّ','ضدِّ','ضمن','طبعا','طبقِ','طبیعتا',
                        'طرف','طريق','طریق','طور','طي','طی','ظاهرا','عدم','عقبِ','علّتِ','علیه','عمدا',
                        'عمدتا','عمل','عملا','عنوان','عنوانِ','غالبا','غير','غیر','فردا','فعلا','فقط','فكر',
                        'فوق','قابل','قبل','قبلا','قدری','قصدِ','قطعا','كرد','كردم','كردن','كردند','كرده',
                        'كسي','كل','كمتر','كند','كنم','كنند','كنيد','كنيم','كه','لااقل','لطفا','لطفاً','ما',
                        'مان','مانند','مانندِ','مبادا','متاسفانه','متعاقبا','مثل','مثلا','مثلِ','مجانی','مجددا',
                        'مجموعا','مختلف','مدام','مدت','مدّتی','مردم','مرسی','مستقیما','مسلما','مطمینا','معمولا',
                        'مقابل','ممکن','من','موارد','مورد','موقتا','مي','ميليارد','ميليون','مگر','می','می شود',
                        'میان','می‌رسد','می‌رود','می‌شود','می‌کنیم','ناشي','نام','ناگاه','ناگهان','ناگهانی','نبايد',
                        'نباید','نبود','نخست','نخستين','نخواهد','نخواهم','نخواهند','نخواهی','نخواهید','نخواهیم',
                        'ندارد','ندارم','ندارند','نداری','ندارید','نداریم','نداشت','نداشتم','نداشتند','نداشته',
                        'نداشتی','نداشتید','نداشتیم','نزديك','نزدِ','نزدیکِ','نسبتا','نشان','نشده','نظير','نظیر',
                        'نكرده','نمايد','نمي','نمی','نمی‌شود','نه','نهایتا','نوع','نوعي','نوعی','نيز','نيست','نگاه',
                        'نیز','نیست','ها','هاي','هايي','های','هایی','هبچ','هر','هرچه','هرگز','هزار','هست','هستم',
                        'هستند','هستيم','هستی','هستید','هستیم','هفت','هم','همان','همه','همواره','همين','همچنان',
                        'همچنين','همچنین','همچون','همیشه','همین','هنوز','هنگام','هنگامِ','هنگامی','هيچ','هیچ','هیچگاه',
                        'و','واقعا','واقعی','وجود','وسطِ','وضع','وقتي','وقتی','وقتیکه','ولی','وي','وگو','وی','ویژه',
                        'يا','يابد','يك','يكديگر','يكي','ّه','٪','پارسال','پاعینِ','پس','پنج','پيش','پیدا','پیش','پیشاپیش',
                        'پیشتر','پیشِ','چرا','چطور','چقدر','چنان','چنانچه','چنانکه','چند','چندین','چنين','چنین','چه',
                        'چهار','چو','چون','چيزي','چگونه','چیز','چیزی','چیست','کاش','کامل','کاملا','کتبا','کجا','کجاست',
                        'کدام','کرد','کردم','کردن','کردند','کرده','کردی','کردید','کردیم','کس','کسانی','کسی','کل','کلا',
                        'کم','کماکان','کمتر','کمتری','کمی','کن','کنار','کنارِ','کند','کنم','کنند','کننده','کنون','کنونی',
                        'کنی','کنید','کنیم','که','کو','کَی','کی','گاه','گاهی','گذاري','گذاشته','گذشته','گردد','گرفت','گرفتم','ﻣﯽ',
                        'گرفتن','گرفتند','گرفته','گرفتی','گرفتید','گرفتیم','گروهي','گفت','گفتم','گفتن','گفتند','گفته','گفتی','ﺑﺮاي',
                        'گفتید','گفتیم','گه','گهگاه','گو','گويد','گويند','گویا','گوید','گویم','گویند','گویی','گویید','گوییم','ﮔﯿﺮد',
                        'گيرد','گيري','گیرد','گیرم','گیرند','گیری','گیرید','گیریم','ی','یا','یابد','یابم','یابند','یابی','یابید','ﮐﻪ',
                        'یابیم','یافت','یافتم','یافتن','یافته','یافتی','یافتید','یافتیم','یعنی','یقینا','یه','یک','یکی','۰','۱','١','ﺷﻮﻧﺪ',
                        '۲','۳','۴','۵','۶','۷','۸','۹','0','1','2','3','4','5','6','7','8','9','[', ']', 'ﻛﻪ', 'ﻫﻤﻴﻦ', 'راﺳﺘﺎ', 'ﭘﺮدازش', 'ﭘﺮس',
                        'ﺟﻮ', 'ي', 'ﺗﻮزﻳﻊ', 'ﺷﺪه', 'ﺑﺎ', 'ﺗﻮﺟﻪ', 'ﺑﻪ', 'اﻳﻨﻜﻪ', 'ﻫﺪف', 'ﻛﻢ', 'ﻛﺮدن', 'ﻳﺎ', 'ﺑﻪ', 'ﺣﺪاﻗﻞ', 'رﺳﺎﻧﺪن','ﻫﺎ','ﺑﺎﺷﺪ',
                        'ﺷﻮد.در','ﻛﻨﻴﻢ','ﻧﻤﻮد','ﻫﺎي','ﻳﻚ','ﺷﻮد','زﻳﺮ','اﻳﻦ','راﺑﻄﻪ','ﺳﺎزي','ﺳﺎﻳﺖ','ﻓﻀﺎي','اﺳﺘﻔﺎده','ﻣﺤﻠﻲ','وﺟﻮ','ﺻﻮرت',
                        'زﻣﺎن','ﻧﻮع','زﻳﺮﭘﺮس','ﺟﻮي']
            filtered_words = [word for word in words if word not in stopWord]
            word_counts = Counter(filtered_words)
            most_common_word = word_counts.most_common(1)
            if most_common_word:
                word, count = most_common_word[0]
                sentences = cleaned_text.split('.')
                sentences_with_common_word = [sentence for sentence in sentences if word in word_tokenize(sentence)]
                body = '.'.join(sentence.strip() for sentence in sentences_with_common_word)

            else:
                print("لیست خالی است.")
                

        form.initial['body'] = body
        form.initial['lang'] = language

        return render(request, 'review.html', {'form':form, 'lang': language})