from django.db import models
from django.shortcuts import reverse
from ckeditor.fields import RichTextField



class Release(models.Model):
    year = models.CharField(max_length=4, db_index=True, verbose_name='Дата выхода')

    def __str__(self):
        return self.year

    class Meta:
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'
        ordering = ['-year']

  #  def get_absolute_url(self):
  #      return reverse('year_detail', kwargs={'slug': self.year})


class Author(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Имя')
    description = RichTextField(blank=True, db_index=True, verbose_name='Описание')
    url = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to="authors/", null=True, blank=True, verbose_name='Фото автора')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name'] 

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'slug': self.url})


class Publisher(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    description = RichTextField(blank=True, db_index=True, verbose_name='Описание')
    url = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to="publishers/", null=True, blank=True, verbose_name='Фото бренда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'
        ordering = ['name'] 
      
    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs={'slug': self.url})


CATEGORIES = (
    (1, 'Русский'),
    (2, 'Английский')
)


def generate_filename(instance, filename):
    filename = instance.slug + '.pdf'
    return "{0}/{1}".format(instance, filename)


def generate_filename_jpg(instance, filename):
    filename = instance.slug + '.webp'
    return "{0}/{1}".format(instance, filename)


class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='Ссылка')
    author = models.ManyToManyField('Author', null=True, related_name='author_books', verbose_name='Автор')
    release_date = models.CharField(max_length=200, blank=True, db_index=True, verbose_name='Год выхода')    
    release = models.ManyToManyField('Release', null=True, related_name='release_books', verbose_name='Дата выхода')
    publisher_book = models.ManyToManyField('Publisher', null=True, related_name='publisher_books', verbose_name='Издательство')
    book_pages = models.CharField(max_length=200, verbose_name='Количество страниц')
    codes = models.CharField(max_length=200, null=True, blank=True, verbose_name='Исходный код')
    description = RichTextField(blank=True, db_index=True, verbose_name='Описание')
    category = models.ManyToManyField('Category', related_name='books', verbose_name='Категория')
    lang_category = models.IntegerField(choices=CATEGORIES, default=1, db_index=True, verbose_name='Язык')
    book_file = models.FileField(upload_to=generate_filename, null=True, verbose_name='Файл PDF')
    img_file = models.ImageField(upload_to=generate_filename_jpg, null=True, verbose_name='Обложка')
    virus_total = models.CharField(max_length=300, blank=True, verbose_name='Virus Total')
    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.title
        
    def get_model_name(self):
        return 'Книга'


    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('book_detail_url', kwargs={'slug': self.slug})


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



