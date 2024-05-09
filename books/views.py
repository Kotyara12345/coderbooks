from django.shortcuts import render, redirect
from video.models import Course
from articles.models import Articles
from booklist.models import Book, Category
from django.core.paginator import Paginator
from django.views import View
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.conf import settings

def main_page(request):
    return redirect('/')

class SearchView(View):
    template_name = 'search.html'

    def get(self, request, *args, **kwargs):
        categories_queryset = Category.objects.all()
        preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else 'en'
        question = request.GET.get('search')
        context = {
            'categories': categories_queryset,
            'lang': lang,
        }
        if not question or len(question) < 3:
            return render(request, 'search_error.html', context=context)

        books = Book.objects.filter(title__icontains=question)
        courses = Course.objects.filter(title__icontains=question)
        articles = Articles.objects.filter(title__icontains=question)
        objects = list(books) + list(courses) + list(articles)

        last_question = '?search=%s' % question

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

        context.update({
            'question': question,
            'last_question': '?search=%s' % question,
            'is_paginated': is_paginated,
            'prev_url': prev_url,
            'next_url': next_url,
            'page_object': page,
        })
        return render(request, self.template_name, context=context)

from django.contrib.syndication.views import Feed

class Rss(Feed):
    title = 'CoderBooks Портал для помощи программистам'
    description = 'Последние опубликованные книги'
    link = '/'

    def items(self):
        return Book.objects.all()

    def item_title(self, item):
        return item.title
        
    def item_description(self, item):
        return item.description

    def item_enclosure_url(self, item):
        return item.img_file.url

def error_404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)

def other_page(request, page):
    categories_queryset = Category.objects.all()
    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    lang = 'ru' if (preferred_language and preferred_language.startswith('ru')) else 'en'
    try:
        template = get_template('booklist/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404

    context = {
        'categories': categories_queryset,
        'lang': lang,
    }  
    return HttpResponse(template.render(context, request=request))

def account_detail(request):
    return render(request, 'account.html')
