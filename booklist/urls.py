from django.urls import path
from .views import book_list
from .views import category_detail
from .views import BookDetail
from . import views
from django.conf.urls import handler404
from .views import error_404

handler404 = error_404

urlpatterns = [
    path('author/<str:slug>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('publisher/<str:slug>/', views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('category/<str:slug>/', category_detail, name='category_detail_url'),
    path('<slug:slug>/', BookDetail.as_view(), name='book_detail_url'),
    path('', book_list, name='book_list_url'),
]


