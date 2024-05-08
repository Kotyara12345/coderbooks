from django.contrib import admin
from .models import Book, Category, Author, Publisher, Release

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'lang_category', 'author_list', 'publisher_book_list', 'release_date', 'release_list')

    def publisher_book_list(self, obj):
        return ", ".join([publisher_book.name for publisher_book in obj.publisher_book.all()])
    publisher_book_list.short_description = 'Издательства' 
    
    def author_list(self, obj):
        return ", ".join([author.name for author in obj.author.all()])
    author_list.short_description = 'Авторы' 

        
    def release_list(self, obj):
        return ", ".join([release.year for release in obj.release.all()])
    release_list.short_description = 'Релиз' 
    
    list_filter = ('created', 'category', 'publisher_book', 'author', 'release_date')
    search_fields = ('title', 'description', 'author_book')
    prepopulated_fields = {'slug': ('title',)}





@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('year',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}    
    search_fields = ('name',)



admin.site.site_title = "CoderBooks"
admin.site.site_header = "CoderBooks"



