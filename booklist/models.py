from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField

CATEGORIES = (
    (1, 'Русский'),
    (2, 'Английский')
)


def generate_filename(instance, filename):
    filename = instance.slug + '.pdf'
    return "{0}/{1}".format(instance, filename)


def generate_filename_jpg(instance, filename):
    filename = instance.slug + '.jpg'
    return "{0}/{1}".format(instance, filename)


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='Ссылка')
    author_book = models.CharField(max_length=200, db_index=True, verbose_name='Автор')
    release_date = models.CharField(max_length=200, db_index=True, verbose_name='Год выхода')
    publisher = models.CharField(max_length=200, verbose_name='Издательство')
    book_pages = models.CharField(max_length=200, verbose_name='Количество страниц')
    codes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Исходный код')
    description = RichTextField(blank=True, db_index=True, verbose_name='Описание')
    desc_for_find = models.TextField(blank=True, db_index=True, verbose_name='Описание для поиска')
    keywords = models.CharField(max_length=200, blank=True, verbose_name='Кейвордс')
    category = models.ManyToManyField('Category', related_name='books', verbose_name='Категория')
    lang_category = models.IntegerField(choices=CATEGORIES, default=1, db_index=True, verbose_name='Язык')
    book_file = models.FileField(upload_to=generate_filename, null=True, blank=True, verbose_name='Файл PDF')
    img_file = models.ImageField(upload_to=generate_filename_jpg, null=True, blank=True, verbose_name='IMG')
    virus_total = models.CharField(max_length=300, blank=True, verbose_name='Virus Total')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def get_model_name(self):
        return 'Книга'

    def get_absolute_url(self):
        cat_name = self.category.first().slug
        return reverse('book_detail_url', kwargs={'slug': self.slug, 'cat_name': cat_name})

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created']

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    desc_for_find_cat = models.TextField(blank=True, db_index=True, verbose_name='Описание для поиска')
    keywords_cat = models.CharField(max_length=200, blank=True, verbose_name='Кейвордс')

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title



