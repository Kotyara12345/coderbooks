from django.urls import path
from .views import BookView
from .views import CategoryView
from .views import BookDetail
from .views import ReleaseView
from . import views
from django.conf.urls import handler404
from .views import error_404

handler404 = error_404

urlpatterns = [
    path('release/<str:slug>/', views.ReleaseView.as_view(), name='release_books'),
    path('author/<str:slug>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('publisher/<str:slug>/', views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('category/<str:slug>/', views.CategoryView.as_view(), name='category_detail_url'),
    path('<slug:slug>/', views.BookDetail.as_view(), name='book_detail_url'),
    path('', BookView.as_view(), name='book_list_url'),
]



