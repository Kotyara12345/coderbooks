from django import forms
from .models import Book, CATEGORIES




class BookFilterForm(forms.Form):

    def get_choices():
        choices = [(None, 'Все авторы')]
        choices += [(value, value) for value in Book.objects.values_list('author_book', flat=True)]
        uniq_choices = list(set(choices)) 
        return uniq_choices


    def get_choices_date():
        choices_date = [(None, '----------')]
        choices_date += [(value, value) for value in Book.objects.values_list('release_date', flat=True)]
        uniq_choices_date = list(set(choices_date))       
        return uniq_choices_date

    
    LANG_CHOICES = [
        ('', 'Все языки'),
        (1, 'Русский'),
        (2, 'Английский')
    ]

    author_book = forms.ChoiceField(choices=get_choices, required=False,  widget=forms.Select(attrs={'class': 'form-select'}), label='Автор')
    lang_category = forms.ChoiceField(required=False, choices=LANG_CHOICES,  widget=forms.Select(attrs={'class': 'form-select'}), label='Выберете язык')
    release_date = forms.ChoiceField(choices=get_choices_date, required=False,  widget=forms.Select(attrs={'class': 'form-select'}), label='Год издания')
