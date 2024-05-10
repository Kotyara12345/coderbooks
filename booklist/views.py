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


class LanguageContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        preferred_language = self.request.META.get('HTTP_ACCEPT_LANGUAGE')
        if preferred_language:
            lang = 'ru' if preferred_language.startswith('ru') else 'en'
        else:
            lang = settings.LANGUAGE_CODE
        context['lang'] = lang
        return context

class BookView(LanguageContextMixin, ListView):
    model = Book
    queryset = Book.objects.all()
    paginate_by = 24


class BookDetail(LanguageContextMixin, DetailView):
    model = Book
    slug_field = 'slug'

class CategoryView(LanguageContextMixin, ListView):
    model = Book
    template_name = 'booklist/category_detail.html'
    context_object_name = 'books'
    category = None
    paginate_by = 24
    
    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Book.objects.all().filter(category__slug=self.category.slug)
        return queryset


class AuthorDetailView(LanguageContextMixin, DetailView):
    model = Author
    slug_field = 'url'
    

class PublisherDetailView(LanguageContextMixin, DetailView):
    model = Publisher
    slug_field = 'url'


class ReleaseView(LanguageContextMixin, ListView):
    model = Release
    template_name = 'booklist/release_detail.html'
    context_object_name = 'books'
    release = None
    paginate_by = 24
    
    def get_queryset(self):
        self.release = Release.objects.get(year=self.kwargs['slug'])
        queryset = Book.objects.all().filter(release__year=self.release.year)
        return queryset
