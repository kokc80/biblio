from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from datetime import date
from apps.authors.models import Author
from apps.books.models import Book


class BookModelTest(TestCase):
    """Тесты для модели Book"""
    def setUp(self):
        """Создание тестовых данных перед каждым тестом"""
        self.author = Author.objects.create(
            first_name="Лев",
            last_name="Толстой",
            birth_date=date(1828, 9, 9)
        )

        self.book_data = {
            "title": "Война и мир",
            "author": self.author,
            "isbn": "9785170909052",
            "genre": "FICTION",
            "publication_year": 1869,
            "publisher": "Русский вестник",
            "description": "Великий роман-эпопея",
            "total_copies": 5,
            "available_copies": 5
        }
        self.book = Book.objects.create(**self.book_data)


    # ----- Тесты создания -----
    def test_create_book_with_all_fields(self):
        """Тест: создание книги со всеми полями"""
        book = Book.objects.create(
            title="Преступление и наказание",
            author=self.author,
            isbn="9785170921481",
            genre="FICTION",
            publication_year=1866,
            publisher="Русский вестник",
            description="Роман о преступлении и наказании",
            total_copies=3,
            available_copies=3
        )

        self.assertEqual(book.title, "Преступление и наказание")
        self.assertEqual(book.author, self.author)
        self.assertEqual(book.isbn, "9785170921481")
        self.assertEqual(book.genre, "FICTION")
        self.assertEqual(book.publication_year, 1866)
        self.assertEqual(book.publisher, "Русский вестник")
        self.assertEqual(book.description, "Роман о преступлении и наказании")
        self.assertEqual(book.total_copies, 3)
        self.assertEqual(book.available_copies, 3)
        self.assertIsNotNone(book.created_at)
        self.assertIsNotNone(book.updated_at)

#     def test_create_book_with_minimal_data(self):
#         """Тест: создание книги с минимальными данными"""
#         book = Book.objects.create(
#             title="Анна Каренина",
#             author=self.author,
#             isbn="9785170909045",
#             publication_year=1877
#         )
#
#         self.assertEqual(book.title, "Анна Каренина")
#         self.assertEqual(book.author, self.author)
#         self.assertEqual(book.isbn, "9785170909045")
#         self.assertEqual(book.publication_year, 1877)
#         # Проверяем значения по умолчанию
#         self.assertEqual(book.genre, "OTHER")
#         self.assertEqual(book.publisher, "")
#         self.assertEqual(book.description, "")
#         self.assertEqual(book.total_copies, 1)
#         self.assertEqual(book.available_copies, 1)
#
    def test_create_book_without_title_should_fail(self):
        """Тест: создание книги без названия должно вызвать ошибку"""
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title=None,
                author=self.author,
                isbn="9785170909045",
                publication_year=1877
            )

    def test_create_book_without_author_should_fail(self):
        """Тест: создание книги без автора должно вызвать ошибку"""
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Тестовая книга",
                author=None,
                isbn="9785170909045",
                publication_year=1877
            )

    def test_create_book_without_isbn_should_fail(self):
        """Тест: создание книги без ISBN должно вызвать ошибку"""
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Тестовая книга",
                author=self.author,
                isbn=None,
                publication_year=1877
            )

    def test_create_book_without_publication_year_should_fail(self):
        """Тест: создание книги без года публикации должно вызвать ошибку"""
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Тестовая книга",
                author=self.author,
                isbn="9785170909045",
                publication_year=None
            )

    # ----- Тесты уникальности ISBN -----
    def test_isbn_unique_constraint(self):
        """Тест: ISBN должен быть уникальным"""
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Другая книга",
                author=self.author,
                isbn=self.book_data["isbn"],  # Тот же ISBN
                publication_year=1900
            )

    # ----- Тесты жанров -----
    def test_genre_choices(self):
        """Тест: проверка всех доступных жанров"""
        genres = ["FICTION", "NON_FICTION", "SCIENCE", "FANTASY",
                  "MYSTERY", "ROMANCE", "HISTORY", "BIOGRAPHY", "POETRY", "OTHER"]

        for i, genre in enumerate(genres):
            # Генерируем уникальный ISBN длиной ровно 13 символов
            isbn = f"978517090{i:04d}"  # Например: 9785170900000, 9785170900001, ...
            # Или: isbn = f"978517090{str(i).zfill(4)}"

            book = Book.objects.create(
                title=f"Книга жанра {genre}",
                author=self.author,
                isbn=isbn,  # 👈 Теперь длина всегда 13 символов
                genre=genre,
                publication_year=2000
            )
            self.assertEqual(book.genre, genre)

    def test_genre_default(self):
        """Тест: жанр по умолчанию - OTHER"""
        book = Book.objects.create(
            title="Книга без жанра",
            author=self.author,
            isbn="9785170909999",
            publication_year=2000
        )
        self.assertEqual(book.genre, "OTHER")

    # ----- Тесты строкового представления -----
    def test_str_method(self):
        """Тест: метод __str__ возвращает название книги"""
        book = Book(title="Война и мир", author=self.author)
        self.assertEqual(str(book), "Война и мир")

    # ----- Тесты метода is_available -----
    def test_is_available_true(self):
        """Тест: is_available() возвращает True, если есть доступные копии"""
        book = Book.objects.create(
            title="Доступная книга",
            author=self.author,
            isbn="9785170909007",
            publication_year=2000,
            total_copies=5,
            available_copies=3
        )
        self.assertTrue(book.is_available())

    def test_is_available_false(self):
        """Тест: is_available() возвращает False, если нет доступных копий"""
        book = Book.objects.create(
            title="Недоступная книга",
            author=self.author,
            isbn="9785170908008",
            publication_year=2000,
            total_copies=5,
            available_copies=0
        )
        self.assertFalse(book.is_available())

