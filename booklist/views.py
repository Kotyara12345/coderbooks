from django.shortcuts import render
from .models import *
from .utils import *
from django.views.generic import View, ListView, DetailView
from django.core.paginator import Paginator

from .forms import BookFilterForm

from .filters import BookFilter
from django.conf import settings

def error_404(request, exception):
    categories = Category.objects.all()

    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if preferred_language:
        lang = 'ru' if preferred_language.startswith('ru') else 'en'
    else:
        lang = settings.LANGUAGE_CODE 

    context = {
        'categories': categories,
        'lang': lang,
    }
    
    return render(request, 'booklist/404.html', status=404, context=context)

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if preferred_language:
        lang = 'ru' if preferred_language.startswith('ru') else 'en'
    else:
        lang = settings.LANGUAGE_CODE # Используем язык, указанный в настройках Django
    #lang = 'ru' if preferred_language.startswith('ru') else 'en'

    
    form = BookFilterForm(request.GET)
    filtered_queryset = BookFilter(request.GET, queryset=books)


    if form.is_valid():
        if form.cleaned_data['lang_category']:
            books = books.filter(lang_category__icontains=form.cleaned_data['lang_category'])
        if form.cleaned_data['author_book']:
            books = books.filter(author_book__regex=form.cleaned_data['author_book'])        
        if form.cleaned_data['release_date']:
            books = books.filter(release_date__icontains=form.cleaned_data['release_date'])

    
    filterset_class = BookFilter         
            
    
    
    # Пагинатор начало
    paginator = Paginator(books, 24)
    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    # Пагинатор конец

    context = {
        'books': books,
        'categories': categories,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'page_object': page,
        'form': form,
        'lang': lang,
    }
    return render(request, 'booklist/booklist.html', context=context)


class BookDetail(ObjectDetailMixin, View):
    model = Book
    template = 'booklist/book_detail.html'



def category_detail(request, slug):
    categories = Category.objects.all()
    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if preferred_language:
        lang = 'ru' if preferred_language.startswith('ru') else 'en'
    else:
        lang = settings.LANGUAGE_CODE # Используем язык, указанный в настройках Django
    #lang = 'ru' if preferred_language.startswith('ru') else 'en'
    context = {
        'categories': categories,
        'lang': lang,
    }
    
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return render(request, 'booklist/404.html', context=context)
    

    books = Book.objects.filter(category=category)


    


    form = BookFilterForm(request.GET)
    filtered_queryset = BookFilter(request.GET, queryset=books)


    if form.is_valid():
        if form.cleaned_data['lang_category']:
            books = books.filter(lang_category__icontains=form.cleaned_data['lang_category'])
        if form.cleaned_data['author_book']:
            books = books.filter(author_book__regex=form.cleaned_data['author_book'])        
        if form.cleaned_data['release_date']:
            books = books.filter(release_date__icontains=form.cleaned_data['release_date'])

    
    filterset_class = BookFilter 
    
    # Пагинатор начало
    paginator1 = Paginator(books, 24)
    page_number1 = request.GET.get('page', default=1)
    page1 = paginator1.get_page(page_number1)
    is_paginated1 = page1.has_other_pages()

    if page1.has_previous():
        prev_url1 = '?page={}'.format(page1.previous_page_number())
    else:
        prev_url1 = ''

    if page1.has_next():
        next_url1 = '?page={}'.format(page1.next_page_number())
    else:
        next_url1 = ''
    # Пагинатор конец



    context = {
        'category': category,
        'categories': categories,
        'books': books,
        'page_object1': page1,
        'is_paginated1': is_paginated1,
        'prev_url1': prev_url1,
        'next_url1': next_url1,
        'paginator1': paginator1,
        'form': form,        
        'lang': lang,
    }
    return render(request, 'booklist/category_detail.html', context=context)


#class AuthorDetailView(DetailView):
#    model = Author
#    slug_field = 'url'
    
class AuthorDetailView(View):
    def get(self, request, slug):
        author = Author.objects.get(url=slug)
        categories = Category.objects.all()
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if preferred_language:
            lang = 'ru' if preferred_language.startswith('ru') else 'en'
        else:
            lang = settings.LANGUAGE_CODE
        context = {
            'categories': categories,
            'author': author,
            'lang': lang,
        }
        
        return render(request, 'booklist/author_detail.html', context=context)




#class PublisherDetailView(DetailView):
#    model = Publisher
#    slug_field = 'url'
class PublisherDetailView(View):   
    def get(self, request, slug):
        publisher_book = Publisher.objects.get(url=slug)
        categories = Category.objects.all()
       
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if preferred_language:
            lang = 'ru' if preferred_language.startswith('ru') else 'en'
        else:
            lang = settings.LANGUAGE_CODE
            
        context = {
            'categories': categories,
            'publisher_book': publisher_book,
            'lang': lang,
        }
        
        return render(request, 'booklist/publisher_detail.html', context=context)


def release_detail(request, slug):      
    release = Release.objects.get(year=slug)
    books = Book.objects.filter(release=release)
    categories = Category.objects.all()
    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else settings.LANGUAGE_CODE
        
    paginator = Paginator(books, 24)
    page_number = request.GET.get('page', default=1)
    page2 = paginator.get_page(page_number)
    is_paginated2 = page2.has_other_pages()

    prev_url = '?page={}'.format(page2.previous_page_number()) if page2.has_previous() else ''
    next_url = '?page={}'.format(page2.next_page_number()) if page2.has_next() else ''

    context = {
        'books': books,
        'categories': categories,
        'release': release,
        'lang': lang,
        'page_object2': page2,
        'is_paginated2': is_paginated2,
        'prev_url': prev_url,
        'next_url': next_url,
    }
        
    return render(request, 'booklist/release_detail.html', context=context)
