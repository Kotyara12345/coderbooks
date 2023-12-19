import django_filters
from .models import Book, CATEGORIES
 
class BookFilter(django_filters.FilterSet):



    lang_category = django_filters.ChoiceFilter(choices=CATEGORIES)
    author_book = django_filters.ModelChoiceFilter(queryset='Book.author_book')
    release_date = django_filters.ModelChoiceFilter(queryset='Book.release_date') 
 
    class Meta:
        model = Book
        fields = ['lang_category', 'author_book', 'release_date']

