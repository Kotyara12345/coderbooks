from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import main_page, SearchView

from django.views.generic.base import RedirectView


from django.contrib.sitemaps.views import sitemap
from books.sitemaps import *
from django.template.loader import get_template
from .views import Rss, account_detail
from .views import other_page

from django.urls import reverse_lazy


from django.conf.urls import handler404
from booklist.views import error_404

handler404 = error_404


#handler404 = 'books.views.error_404'

sitemaps = {
    'author': AuthorSitemap,
    'publisher': PublisherSitemap,
    'books_category': BookCategorySitemap,
    'books': BookSitemap,
    'static': StaticViewSitemap
}

urlpatterns = [
    path('sitemaps.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('books/', RedirectView.as_view(url='/', permanent=True)),
    path('rss.xml', Rss(), name='rss_url'),
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search_url'),
    path('', include('booklist.urls')),     
    path('page/<str:page>/', other_page, name='other'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
