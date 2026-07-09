from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления книгами.
    Поддерживает:
    - CRUD операции
    - Фильтрацию по author, genre, publication_year
    - Поиск по title, author__first_name, author__last_name
    - Сортировку по title, publication_year, created_at
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Настройка фильтров
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'author': ['exact'],
        'genre': ['exact'],
        'publication_year': ['exact', 'lt', 'gt', 'lte', 'gte'],
        'available_copies': ['exact', 'gt', 'lt'],
    }
    search_fields = ['title', 'author__first_name', 'author__last_name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']
