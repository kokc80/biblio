from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authors.models import Author
from books.models import Book

User = get_user_model()


class BookAPITest(TestCase):
    """Тесты для API книг"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        # Очищаем данные перед каждым тестом
        Book.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()

        self.client = APIClient()

        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        # Создаем автора
        self.author = Author.objects.create(
            first_name="Лев",
            last_name="Толстой",
            birth_date=date(1828, 9, 9)
        )

        # Создаем тестовую книгу
        self.book = Book.objects.create(
            title="Война и мир",
            author=self.author,
            isbn="9785170909052",
            genre="FICTION",
            publication_year=1869,
            publisher="Русский вестник",
            description="Великий роман-эпопея",
            total_copies=5,
            available_copies=5
        )

        # URL для API
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book.id])

    def tearDown(self):
        """Очистка после каждого теста"""
        Book.objects.all().delete()
        Author.objects.all().delete()
        User.objects.all().delete()

    # ----- Тесты для списка книг (GET /books/) -----
    def test_get_books_list_authenticated(self):
        """Тест: получение списка книг авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Война и мир")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Война и мир")

    def test_get_books_list_unauthenticated(self):
        """Тест: получение списка книг без авторизации (разрешено)"""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_get_books_list_with_filters(self):
        """Тест: фильтрация книг по названию через поиск"""
        # Создаем еще книги
        Book.objects.create(
            title="Анна Каренина",
            author=self.author,
            isbn="9785170909053",
            publication_year=1877
        )
        Book.objects.create(
            title="Другая книга",
            author=self.author,
            isbn="9785170909054",
            publication_year=2000
        )

        self.client.force_authenticate(user=self.user)
        # Используем search вместо title
        response = self.client.get(f"{self.list_url}?search=Война")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Война и мир")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Война и мир")

    def test_get_books_list_filter_by_author(self):
        """Тест: фильтрация книг по автору"""
        author2 = Author.objects.create(
            first_name="Фёдор",
            last_name="Достоевский"
        )
        # Создаем книги для второго автора
        Book.objects.create(
            title="Преступление и наказание",
            author=author2,
            isbn="9785170909054",
            publication_year=1866
        )
        Book.objects.create(
            title="Идиот",
            author=author2,
            isbn="9785170909055",
            publication_year=1869
        )
        # Создаем еще одну книгу для первого автора
        Book.objects.create(
            title="Анна Каренина",
            author=self.author,
            isbn="9785170909056",
            publication_year=1877
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.list_url}?author={author2.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            # Должно быть 2 книги Достоевского
            self.assertEqual(len(response.data['results']), 2)
            for book in response.data['results']:
                self.assertEqual(book['author'], author2.id)
        else:
            self.assertEqual(len(response.data), 2)
            for book in response.data:
                self.assertEqual(book['author'], author2.id)

    def test_get_books_list_filter_by_genre(self):
        """Тест: фильтрация книг по жанру"""
        # Создаем книги разных жанров
        Book.objects.create(
            title="Фантастическая книга",
            author=self.author,
            isbn="9785170909055",
            genre="FANTASY",
            publication_year=2000
        )
        Book.objects.create(
            title="Детективная книга",
            author=self.author,
            isbn="9785170909056",
            genre="MYSTERY",
            publication_year=2000
        )
        Book.objects.create(
            title="Научная книга",
            author=self.author,
            isbn="9785170909057",
            genre="SCIENCE",
            publication_year=2000
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.list_url}?genre=FANTASY")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            # Должна быть только одна книга жанра FANTASY
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['genre'], "FANTASY")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['genre'], "FANTASY")

    def test_get_books_list_filter_by_publication_year(self):
        """Тест: фильтрация книг по году публикации"""
        # Создаем книги разных годов
        Book.objects.create(
            title="Книга 1869",
            author=self.author,
            isbn="9785170909057",
            publication_year=1869
        )
        Book.objects.create(
            title="Книга 1877",
            author=self.author,
            isbn="9785170909058",
            publication_year=1877
        )
        Book.objects.create(
            title="Книга 2000",
            author=self.author,
            isbn="9785170909059",
            publication_year=2000
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.list_url}?publication_year=1869")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            # Должны быть книги только 1869 года (Война и мир + созданная)
            self.assertEqual(len(response.data['results']), 2)
            for book in response.data['results']:
                self.assertEqual(book['publication_year'], 1869)
        else:
            self.assertEqual(len(response.data), 2)
            for book in response.data:
                self.assertEqual(book['publication_year'], 1869)

    def test_get_books_list_search(self):
        """Тест: поиск книг по названию"""
        # Создаем книги для поиска
        Book.objects.create(
            title="Война и мир (том 2)",
            author=self.author,
            isbn="9785170909060",
            publication_year=1870
        )
        Book.objects.create(
            title="Анна Каренина",
            author=self.author,
            isbn="9785170909061",
            publication_year=1877
        )
        Book.objects.create(
            title="Детская книга",
            author=self.author,
            isbn="9785170909062",
            publication_year=2000
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.list_url}?search=Война")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            # Должны быть книги с "Война" в названии (2 штуки)
            self.assertEqual(len(response.data['results']), 2)
            for book in response.data['results']:
                self.assertIn("Война", book['title'])
        else:
            self.assertEqual(len(response.data), 2)
            for book in response.data:
                self.assertIn("Война", book['title'])

    def test_get_books_list_search_by_author(self):
        """Тест: поиск книг по фамилии автора"""
        author2 = Author.objects.create(
            first_name="Фёдор",
            last_name="Достоевский"
        )
        # Создаем книги для Достоевского
        Book.objects.create(
            title="Преступление и наказание",
            author=author2,
            isbn="9785170909062",
            publication_year=1866
        )
        Book.objects.create(
            title="Братья Карамазовы",
            author=author2,
            isbn="9785170909063",
            publication_year=1880
        )
        # Создаем книгу для Толстого
        Book.objects.create(
            title="Анна Каренина",
            author=self.author,
            isbn="9785170909064",
            publication_year=1877
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.list_url}?search=Достоевский")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            # Должны быть только книги Достоевского (2 штуки)
            self.assertEqual(len(response.data['results']), 2)
            for book in response.data['results']:
                self.assertEqual(book['author'], author2.id)
        else:
            self.assertEqual(len(response.data), 2)
            for book in response.data:
                self.assertEqual(book['author'], author2.id)

    def test_get_books_list_ordering(self):
        """Тест: сортировка книг"""
        # Создаем книги с разными названиями
        Book.objects.create(
            title="Анна Каренина",
            author=self.author,
            isbn="9785170909063",
            publication_year=1877
        )
        Book.objects.create(
            title="Воскресение",
            author=self.author,
            isbn="9785170909064",
            publication_year=1899
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"{self.list_url}?ordering=title")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        if 'results' in response.data:
            titles = [book['title'] for book in response.data['results']]
            self.assertEqual(titles, sorted(titles))
        else:
            titles = [book['title'] for book in response.data]
            self.assertEqual(titles, sorted(titles))
