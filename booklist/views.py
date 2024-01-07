from django.shortcuts import render
from .models import *
from .utils import *
from django.views.generic import View
from django.core.paginator import Paginator

from .forms import BookFilterForm

from .filters import BookFilter
# Create your views here.
def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()


    
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
    paginator = Paginator(books, 20)
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
    }
    return render(request, 'booklist/booklist.html', context=context)


class BookDetail(ObjectDetailMixin, View):
    model = Book
    template = 'booklist/book_detail.html'



def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    categories = Category.objects.all()
    books = Book.objects.filter(category=category)
    if not category:
        return render(request, 'booklist/../templates/404.html', context={})
    


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
    paginator1 = Paginator(books, 20)
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
        'form': form
    }
    return render(request, 'booklist/category_detail.html', context=context)



