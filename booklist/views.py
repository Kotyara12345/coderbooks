from django.shortcuts import render
from .models import *
from .utils import *
from django.views.generic import View
from django.core.paginator import Paginator

from .forms import BookFilterForm
from .filters import BookFilter
from django.conf import settings

def error_404(request, exception):
    categories = Category.objects.all()

    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else settings.LANGUAGE_CODE

    context = {
        'categories': categories,
        'lang': lang,
    }
    
    return render(request, 'booklist/404.html', status=404, context=context)


def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else settings.LANGUAGE_CODE

    form = BookFilterForm(request.GET)
    filtered_queryset = BookFilter(request.GET, queryset=books)

    if form.is_valid():
        books = filtered_queryset.qs

    paginator = Paginator(books, 24)
    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

    context = {
        'books': page,
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
    lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else settings.LANGUAGE_CODE

    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        return render(request, 'booklist/404.html', context={'categories': categories, 'lang': lang})

    books = Book.objects.filter(category=category)
    form = BookFilterForm(request.GET)
    filtered_queryset = BookFilter(request.GET, queryset=books)

    if form.is_valid():
        books = filtered_queryset.qs

    paginator = Paginator(books, 24)
    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
    next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

    context = {
        'category': category,
        'categories': categories,
        'books': page,
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'form': form,
        'lang': lang,
    }
    return render(request, 'booklist/category_detail.html', context=context)


class AuthorDetailView(View):
    def get(self, request, slug):
        author = Author.objects.get(url=slug)
        categories = Category.objects.all()
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else settings.LANGUAGE_CODE

        context = {
            'categories': categories,
            'author': author,
            'lang': lang,
        }
        
        return render(request, 'booklist/author_detail.html', context=context)


class PublisherDetailView(View):   
    def get(self, request, slug):
        publisher_book = Publisher.objects.get(url=slug)
        categories = Category.objects.all()
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else settings.LANGUAGE_CODE
            
        context = {
            'categories': categories,
            'publisher_book': publisher_book,
            'lang': lang,
        }
        
        return render(request, 'booklist/publisher_detail.html', context=context)


class ReleaseDetailView(View):
    def get(self, request, slug):
        release = Release.objects.get(year=slug)
        categories = Category.objects.all()
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else settings.LANGUAGE_CODE
        
        paginator = Paginator(books, 24)
        page_number = request.GET.get('page', default=1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        prev_url = '?page={}'.format(page.previous_page_number()) if page.has_previous() else ''
        next_url = '?page={}'.format(page.next_page_number()) if page.has_next() else ''

        context = {
            'categories': categories,
            'release': release,
            'lang': lang,
            'page_object': page,
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url,
        }
        
        return render(request, 'booklist/release_detail.html', context=context)
