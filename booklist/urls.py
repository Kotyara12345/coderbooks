from django.urls import path
from .views import book_list
from .views import category_detail
from .views import BookDetail


urlpatterns = [
    path('', book_list, name='book_list_url'),
    path('<slug>/', category_detail, name='category_detail_url'),
    path('<cat_name>/<slug>/', BookDetail.as_view(), name='book_detail_url'),
]


