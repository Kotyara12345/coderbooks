from django.contrib import admin
from .models import Book, Category, Comments

# Register your models here.

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Comments)
