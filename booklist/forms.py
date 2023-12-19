from django import forms
from .models import Book, CATEGORIES




class BookFilterForm(forms.Form):

    def get_choices():

        choices = [(None, '----------')]  # Add an empty choice
        choices += [(value, value) for value in Book.objects.values_list('author_book', flat=True)]
        uniq_choices = list(set(choices)) 
        sorted_choices = sorted(uniq_choices, key=lambda x: x[1])   
        
        return sorted_choices

    def get_choices_date():

        choices_date = [(None, '----------')]  # Add an empty choice
        choices_date += [(value, value) for value in Book.objects.values_list('release_date', flat=True)]
        uniq_choices_date = list(set(choices_date))  
        sorted_choices_date = sorted(uniq_choices_date, key=lambda x: x[1])   
        return sorted_choices_date

    LANG_CHOICES = [
        ('', '----------'),
        (1, 'Русский'),
        (2, 'Английский')
    ]

    
    author_book = forms.ChoiceField(choices=get_choices, required=False,  widget=forms.Select(attrs={'class': 'form-select'}), label='Автор')
    lang_category = forms.ChoiceField(required=False, choices=LANG_CHOICES,  widget=forms.Select(attrs={'class': 'form-select'}), label='Выберете язык')
    release_date = forms.ChoiceField(choices=get_choices_date, required=False,  widget=forms.Select(attrs={'class': 'form-select'}), label='Год издания')
