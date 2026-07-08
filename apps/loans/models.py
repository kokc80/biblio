from django.db import models
from django.conf import settings
from apps.books.models import Book
from datetime import date, timedelta


class Loan(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("RETURNED", "Returned"),
        ("OVERDUE", "Overdue"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="loans"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrowed_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-borrowed_date"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=14)
        if self.returned_date and self.status != "RETURNED":
            self.status = "RETURNED"
            self.book.available_copies += 1
            self.book.save()
        super().save(*args, **kwargs)
