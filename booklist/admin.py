from django.contrib import admin
from .models import Book, Category, Author, Publisher, Release



admin.site.register(Book)

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
