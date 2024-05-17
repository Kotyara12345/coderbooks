from django.contrib import admin
from .models import Book, Category, Author, Publisher, Release

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'lang_category', 'author_list', 'publisher_book_list', 'release_list')

    fields = (('title', 'slug'), ('author', 'release', ' publisher_book', 'category'), 'lang_category', 'description', 'book_pages', 'codes', 'book_file', 'img_file', 'virus_total')
    
    def delete_model(self, request, obj):
        obj.book_file.delete()
        obj.delete()

    
    def publisher_book_list(self, obj):
        return ", ".join([publisher_book.name for publisher_book in obj.publisher_book.all()])
    publisher_book_list.short_description = 'Издательства' 
    publisher_book_list.admin_order_field = 'publisher_book__name'
    
    def author_list(self, obj):
        return ", ".join([author.name for author in obj.author.all()])
    author_list.short_description = 'Авторы' 
    author_list.admin_order_field = 'author__name'
        
    def release_list(self, obj):
        return ", ".join([release.year for release in obj.release.all()])
    release_list.short_description = 'Релиз' 
    release_list.admin_order_field = 'release__year'
    
    list_filter = ('created', 'category', 'publisher_book', 'author', 'release')  # Убрал 'release_list', так как это метод, а не поле модели
    search_fields = ('title', 'description')
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

# Настройки административной панели
admin.site.site_title = "CoderBooks"
admin.site.site_header = "CoderBooks"
