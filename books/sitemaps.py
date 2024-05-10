from django.contrib.sitemaps import Sitemap

from booklist.models import Book
from booklist.models import Author
from booklist.models import Publisher
from booklist.models import Category as BookCategory

from django.shortcuts import reverse


class BookSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Book.objects.all()


class AuthorSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Author.objects.all()


class PublisherSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Publisher.objects.all()



class BookCategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return BookCategory.objects.all()


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        # return ['main_page_url', 'book_list_url', 'articles_list_url', 'category_video_list_url']
        return ['book_list_url']

    def location(self, item):
        return reverse(item)


