from django import forms
from .models import Comments, Book


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_text']

        widgets = {
            'comment_text': forms.Textarea(attrs={'class': 'form-control'})
        }


class BookFilterForm(forms.Form):

    def get_choices():
        return [(value, value) for value in Book.objects.values_list('author_book', flat=True)]

    LANG_CHOICES = [
        ('', 'Все языки'),
        (1, 'Русский'),
        (2, 'Английский')
    ]

    author_book = forms.ChoiceField(choices=get_choices, required=False,  widget=forms.Select(attrs={'class': 'form-select'}), label='Автор')
    lang_category = forms.ChoiceField(required=False, choices=LANG_CHOICES,  widget=forms.Select(attrs={'class': 'form-select'}), label='Выберете язык')
