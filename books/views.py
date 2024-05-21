from django.shortcuts import render, redirect
from booklist.models import Book
from booklist.models import Category

from django.core.paginator import Paginator
from django.views import View

from django.http import Http404
from django.http import HttpResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.conf import settings


def main_page(request):
    return redirect('/')


class SearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        if preferred_language:
            lang = 'ru' if preferred_language.startswith('ru') else 'en'
        else:
            lang = settings.LANGUAGE_CODE # Используем язык, указанный в настройках Django
        #lang = 'ru' if preferred_language.startswith('ru') else 'en'
        question = request.GET.get('search')
        context = {
                'categories': categories,
                'lang': lang,
            }
        if not question or len(question) < 3:
            return render(request, 'search_error.html', context=context)
        
           books = Book.objects.filter(Q(title__icontains=question) | Q(author__name__icontains=question) | Q(publisher_book__name__icontains=question))
    objects = list(books) 
        


            last_question = '?search=%s' % question

            # Пагинатор начало
            paginator = Paginator(objects, 15)
            page_number = request.GET.get('page', default=1)
            page = paginator.get_page(page_number)
            is_paginated = page.has_other_pages()

            if page.has_previous():
                prev_url = '{}&page={}'.format(last_question, page.previous_page_number())
            else:
                prev_url = ''

            if page.has_next():
                next_url = '{}&page={}'.format(last_question, page.next_page_number())
            else:
                next_url = ''
            # Пагинатор конец

            context = {
                'question': question,
                'last_question': '?search=%s' % question,
                'is_paginated': is_paginated,
                'prev_url': prev_url,
                'next_url': next_url,
                'page_object': page,
                'categories': categories,
                'lang': lang,

            }
        return render(request, self.template_name, context=context)


#  RSS лента
from django.contrib.syndication.views import Feed


class Rss(Feed):
    title = 'CoderBooks Портал для помощи программистам'
    description = 'Последние опубликованные книги'
    link = '/'

    def items(self):
        # qs = list(Book.objects.all()) + list(Course.objects.all()) + list(Articles.objects.all())
        qs = Book.objects.all()
        return qs

    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.description

    def item_enclosure_url(self, item):
        return item.img_file.url

#  404 кастом

def error_404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)

def other_page(request, page):
    categories = Category.objects.all()
    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if preferred_language:
        lang = 'ru' if preferred_language.startswith('ru') else 'en'
    else:
        lang = settings.LANGUAGE_CODE # Используем язык, указанный в настройках Django
    #lang = 'ru' if preferred_language.startswith('ru') else 'en'
    try:
        template = get_template('booklist/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404

    context = {
        'categories': categories,
        'lang': lang,
    }  
    return HttpResponse(template.render(context, request=request))
    

def account_detail(request):
    return render(request, 'account.html')
