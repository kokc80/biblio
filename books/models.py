from django.db import models

from authors.models import Author


class Book(models.Model):
    GENRE_CHOICES = [
        ("FICTION", "Fiction"),
        ("NON_FICTION", "Non-Fiction"),
        ("SCIENCE", "Science"),
        ("FANTASY", "Fantasy"),
        ("MYSTERY", "Mystery"),
        ("ROMANCE", "Romance"),
        ("HISTORY", "History"),
        ("BIOGRAPHY", "Biography"),
        ("POETRY", "Poetry"),
        ("OTHER", "Other"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор книги", related_name="books")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="Международный стандартный книжный номер")
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, verbose_name="Жанр книги", default="OTHER")
    publication_year = models.IntegerField(verbose_name="Год публикации")
    publisher = models.CharField(max_length=200, blank=True, verbose_name="Публикатор")
    description = models.TextField(blank=True, verbose_name="Примечание")
    total_copies = models.IntegerField(default=1, verbose_name="Количество копий")
    available_copies = models.IntegerField(default=1, verbose_name="Доступные копии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_copies > 0
