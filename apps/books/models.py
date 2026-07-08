from django.db import models
from apps.authors.models import Author


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

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default="OTHER")
    publication_year = models.IntegerField()
    publisher = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def is_available(self):
        return self.available_copies > 0
