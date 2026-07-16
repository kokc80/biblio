from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'genre', 'publication_year', 'available_copies']
    list_filter = ['genre', 'publication_year']
    search_fields = ['title', 'isbn', 'author__first_name', 'author__last_name']
    raw_id_fields = ['author']  # Это упрощает выбор автора
    list_editable = ['available_copies']  # Можно редактировать прямо в списке
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'isbn', 'genre')
        }),
        ('Детали', {
            'fields': ('publication_year', 'publisher', 'description')
        }),
        ('Количество', {
            'fields': ('total_copies', 'available_copies')
        }),
    )
