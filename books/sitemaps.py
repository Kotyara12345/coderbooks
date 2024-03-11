from django.contrib.sitemaps import Sitemap

from booklist.models import Book
from booklist.models import Category as BookCategory
from video.models import Course
from video.models import Category as VideoCategory
from articles.models import Articles
from articles.models import Category as ArticlesCategory

from django.shortcuts import reverse


class ArticleSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Articles.objects.all()


class ArticlesCategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return ArticlesCategory.objects.all()


class CourseSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Course.objects.all()


class VideoCategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return VideoCategory.objects.all()


class BookSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        return Book.objects.all()


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


