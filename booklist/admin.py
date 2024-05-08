from django.contrib import admin
from .models import Book, Category, Author, Publisher

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'lang_category', 'author_book', 'author_list', 'publisher_book', 'release_date')

    def author_list(self, obj):
        return ", ".join([author.name for author in obj.author.all()])
    author_list.short_description = 'Авторы' 
    
    list_filter = ('created', 'category', 'publisher_book', 'author_book')
    search_fields = ('title', 'description', 'author_book')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}
    #search_fields = ('name')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}    
    #search_fields = ('name')



admin.site.site_title = "CoderBooks"
admin.site.site_header = "CoderBooks"



