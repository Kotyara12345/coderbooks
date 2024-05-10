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
    paginate_by = 1


class BookDetail(LanguageContextMixin, DetailView):
    model = Book
    slug_field = 'slug'




class AuthorDetailView(LanguageContextMixin, DetailView):
    model = Author
    slug_field = 'url'
    

class PublisherDetailView(LanguageContextMixin, DetailView):
    model = Publisher
    slug_field = 'url'


class BaseDetailView(LanguageContextMixin, ListView):
    template_name = None
    context_object_name = None
    paginate_by = 24
    key_field = None

    def get_queryset(self):
        key_value = self.kwargs['slug']
        filter_kwargs = {self.key_field: key_value}
        self.instance = self.model.objects.get(**filter_kwargs)
        queryset = self.related_model.objects.filter(**{self.related_field: getattr(self.instance, self.key_field)})
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.key_field] = self.instance
        paginator = context['paginator']
        if paginator.count <= self.paginate_by:
            context['hide_pagination'] = True
        return context

class ReleaseView(BaseDetailView):
    model = Release
    template_name = 'booklist/release_detail.html'
    context_object_name = 'books'
    key_field = 'year'
    related_model = Book
    related_field = 'release__year'

class CategoryView(BaseDetailView):
    model = Category
    template_name = 'booklist/category_detail.html'
    context_object_name = 'books'
    key_field = 'slug'
    related_model = Book
    related_field = 'category__slug'
