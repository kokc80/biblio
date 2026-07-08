from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'genre', 'available_copies']
    search_fields = ['title', 'isbn']
    list_filter = ['genre', 'publication_year']