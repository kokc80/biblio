from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя автора")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия автора")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения автора")
    biography = models.TextField(blank=True, verbose_name="Библиография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
