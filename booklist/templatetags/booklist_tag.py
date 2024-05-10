from django import template
from booklist.models import Category, Book

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()



@register.simple_tag()
def get_lang(self, request, **kwargs):
    preferred_language = request.META.get('HTTP_ACCEPT_LANGUAGE')
    if preferred_language:
        lang = 'ru' if preferred_language.startswith('ru') else 'en'
    else:
        lang = settings.LANGUAGE_CODE

    context = {
        'lang': lang,
    }
