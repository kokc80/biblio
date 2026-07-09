from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from apps.authors.models import Author
from apps.books.models import Book


class BookAPITest(TestCase):
    """Тесты для API книг"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        self.client = APIClient()

        # Создаем тестового пользователя для аутентификации
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

#     # ----- Тесты для списка книг (GET /books/) -----
#     def test_get_books_list_authenticated(self):
#         """Тест: получение списка книг авторизованным пользователем"""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.list_url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], "Война и мир")
#         self.assertEqual(response.data[0]['author'], self.author.id)
#         self.assertEqual(response.data[0]['isbn'], "9785170909052")
#
#     def test_get_books_list_unauthenticated(self):
#         """Тест: получение списка книг без авторизации (разрешено)"""
#         response = self.client.get(self.list_url)
#
#         # IsAuthenticatedOrReadOnly разрешает чтение без авторизации
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_get_books_list_with_pagination(self):
#         """Тест: получение списка с пагинацией"""
#         # Создаем еще 5 книг
#         for i in range(5):
#             Book.objects.create(
#                 title=f"Книга {i}",
#                 author=self.author,
#                 isbn=f"978517090{i:04d}",
#                 publication_year=2000 + i
#             )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.list_url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Если есть пагинация
#         if 'results' in response.data:
#             self.assertTrue(len(response.data['results']) > 0)
#         else:
#             self.assertTrue(len(response.data) >= 1)
#
#     def test_get_books_list_with_filters(self):
#         """Тест: фильтрация книг по названию"""
#         # Создаем еще книгу
#         Book.objects.create(
#             title="Анна Каренина",
#             author=self.author,
#             isbn="9785170909053",
#             publication_year=1877
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?title=Война")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], "Война и мир")
#
#     def test_get_books_list_filter_by_author(self):
#         """Тест: фильтрация книг по автору"""
#         author2 = Author.objects.create(
#             first_name="Фёдор",
#             last_name="Достоевский"
#         )
#         Book.objects.create(
#             title="Преступление и наказание",
#             author=author2,
#             isbn="9785170909054",
#             publication_year=1866
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?author={author2.id}")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], "Преступление и наказание")
#
#     def test_get_books_list_filter_by_genre(self):
#         """Тест: фильтрация книг по жанру"""
#         Book.objects.create(
#             title="Фантастическая книга",
#             author=self.author,
#             isbn="9785170909055",
#             genre="FANTASY",
#             publication_year=2000
#         )
#         Book.objects.create(
#             title="Детективная книга",
#             author=self.author,
#             isbn="9785170909056",
#             genre="MYSTERY",
#             publication_year=2000
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?genre=FANTASY")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['genre'], "FANTASY")
#
#     def test_get_books_list_filter_by_publication_year(self):
#         """Тест: фильтрация книг по году публикации"""
#         Book.objects.create(
#             title="Книга 1869",
#             author=self.author,
#             isbn="9785170909057",
#             publication_year=1869
#         )
#         Book.objects.create(
#             title="Книга 2000",
#             author=self.author,
#             isbn="9785170909058",
#             publication_year=2000
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?publication_year=1869")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)  # Война и мир (1869) + созданная
#
#     def test_get_books_list_filter_by_available(self):
#         """Тест: фильтрация по доступности"""
#         # Создаем недоступную книгу
#         Book.objects.create(
#             title="Недоступная книга",
#             author=self.author,
#             isbn="9785170909059",
#             publication_year=2000,
#             available_copies=0
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?available=true")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Должны быть только доступные книги
#         for book in response.data:
#             self.assertGreater(book['available_copies'], 0)
#
#     def test_get_books_list_search(self):
#         """Тест: поиск книг по названию"""
#         Book.objects.create(
#             title="Война и мир (том 2)",
#             author=self.author,
#             isbn="9785170909060",
#             publication_year=1870
#         )
#         Book.objects.create(
#             title="Анна Каренина",
#             author=self.author,
#             isbn="9785170909061",
#             publication_year=1877
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?search=Война")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)  # Война и мир + том 2
#
#     def test_get_books_list_search_by_author(self):
#         """Тест: поиск книг по фамилии автора"""
#         author2 = Author.objects.create(
#             first_name="Фёдор",
#             last_name="Достоевский"
#         )
#         Book.objects.create(
#             title="Преступление и наказание",
#             author=author2,
#             isbn="9785170909062",
#             publication_year=1866
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?search=Достоевский")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], "Преступление и наказание")
#
#     def test_get_books_list_ordering(self):
#         """Тест: сортировка книг"""
#         Book.objects.create(
#             title="Анна Каренина",
#             author=self.author,
#             isbn="9785170909063",
#             publication_year=1877
#         )
#         Book.objects.create(
#             title="Воскресение",
#             author=self.author,
#             isbn="9785170909064",
#             publication_year=1899
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?ordering=title")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         titles = [book['title'] for book in response.data]
#         self.assertEqual(titles, sorted(titles))
#
#     def test_get_books_list_ordering_by_publication_year(self):
#         """Тест: сортировка по году публикации"""
#         Book.objects.create(
#             title="Анна Каренина",
#             author=self.author,
#             isbn="9785170909065",
#             publication_year=1877
#         )
#         Book.objects.create(
#             title="Воскресение",
#             author=self.author,
#             isbn="9785170909066",
#             publication_year=1899
#         )
#
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(f"{self.list_url}?ordering=publication_year")
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         years = [book['publication_year'] for book in response.data]
#         self.assertEqual(years, sorted(years))
#
#     # ----- Тесты для создания книги (POST /books/) -----
#     def test_create_book_authenticated(self):
#         """Тест: создание книги авторизованным пользователем"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Преступление и наказание",
#             "author": self.author.id,
#             "isbn": "9785170921481",
#             "genre": "FICTION",
#             "publication_year": 1866,
#             "publisher": "Русский вестник",
#             "description": "Роман о преступлении и наказании",
#             "total_copies": 3,
#             "available_copies": 3
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['title'], "Преступление и наказание")
#         self.assertEqual(response.data['author'], self.author.id)
#         self.assertEqual(response.data['isbn'], "9785170921481")
#         self.assertEqual(response.data['genre'], "FICTION")
#         self.assertEqual(Book.objects.count(), 2)
#
#     def test_create_book_unauthenticated(self):
#         """Тест: создание книги без авторизации (запрещено)"""
#         data = {
#             "title": "Преступление и наказание",
#             "author": self.author.id,
#             "isbn": "9785170921481",
#             "publication_year": 1866
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         # IsAuthenticatedOrReadOnly запрещает создание без авторизации
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(Book.objects.count(), 1)
#
#     def test_create_book_with_minimal_data(self):
#         """Тест: создание книги с минимальными данными"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Анна Каренина",
#             "author": self.author.id,
#             "isbn": "9785170909045",
#             "publication_year": 1877
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['title'], "Анна Каренина")
#         self.assertEqual(response.data['author'], self.author.id)
#         self.assertEqual(response.data['isbn'], "9785170909045")
#         self.assertEqual(response.data['publication_year'], 1877)
#         # Проверяем значения по умолчанию
#         self.assertEqual(response.data['genre'], "OTHER")
#         self.assertEqual(response.data['publisher'], "")
#         self.assertEqual(response.data['description'], "")
#         self.assertEqual(response.data['total_copies'], 1)
#         self.assertEqual(response.data['available_copies'], 1)
#
#     def test_create_book_without_title(self):
#         """Тест: создание книги без названия (должно вернуть ошибку)"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "author": self.author.id,
#             "isbn": "9785170909045",
#             "publication_year": 1877
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("title", response.data)
#         self.assertEqual(Book.objects.count(), 1)
#
#     def test_create_book_without_author(self):
#         """Тест: создание книги без автора (должно вернуть ошибку)"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Тестовая книга",
#             "isbn": "9785170909045",
#             "publication_year": 1877
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("author", response.data)
#         self.assertEqual(Book.objects.count(), 1)
#
#     def test_create_book_without_isbn(self):
#         """Тест: создание книги без ISBN (должно вернуть ошибку)"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Тестовая книга",
#             "author": self.author.id,
#             "publication_year": 1877
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("isbn", response.data)
#         self.assertEqual(Book.objects.count(), 1)
#
#     def test_create_book_without_publication_year(self):
#         """Тест: создание книги без года публикации (должно вернуть ошибку)"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Тестовая книга",
#             "author": self.author.id,
#             "isbn": "9785170909045"
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("publication_year", response.data)
#         self.assertEqual(Book.objects.count(), 1)
#
#     def test_create_book_with_duplicate_isbn(self):
#         """Тест: создание книги с существующим ISBN (должно вернуть ошибку)"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Другая книга",
#             "author": self.author.id,
#             "isbn": self.book.isbn,  # Тот же ISBN
#             "publication_year": 2000
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("isbn", response.data)
#         self.assertEqual(Book.objects.count(), 1)
#
#     def test_create_book_with_invalid_genre(self):
#         """Тест: создание книги с недопустимым жанром"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Тестовая книга",
#             "author": self.author.id,
#             "isbn": "9785170909045",
#             "genre": "INVALID_GENRE",
#             "publication_year": 2000
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("genre", response.data)
#         self.assertEqual(Book.objects.count(), 1)
#
#     def test_create_book_with_nonexistent_author(self):
#         """Тест: создание книги с несуществующим автором"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Тестовая книга",
#             "author": 99999,  # Несуществующий ID
#             "isbn": "9785170909045",
#             "publication_year": 2000
#         }
#
#         response = self.client.post(self.list_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("author", response.data)
#         self.assertEqual(Book.objects.count(), 1)
#
#     # ----- Тесты для получения одной книги (GET /books/{id}/) -----
#     def test_get_single_book_authenticated(self):
#         """Тест: получение одной книги авторизованным пользователем"""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.detail_url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['id'], self.book.id)
#         self.assertEqual(response.data['title'], "Война и мир")
#         self.assertEqual(response.data['author'], self.author.id)
#         self.assertEqual(response.data['isbn'], "9785170909052")
#         self.assertEqual(response.data['genre'], "FICTION")
#         self.assertEqual(response.data['publication_year'], 1869)
#         self.assertEqual(response.data['total_copies'], 5)
#         self.assertEqual(response.data['available_copies'], 5)
#
#     def test_get_single_book_unauthenticated(self):
#         """Тест: получение одной книги без авторизации (разрешено)"""
#         response = self.client.get(self.detail_url)
#
#         # IsAuthenticatedOrReadOnly разрешает чтение
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], "Война и мир")
#
#     def test_get_nonexistent_book(self):
#         """Тест: получение несуществующей книги"""
#         self.client.force_authenticate(user=self.user)
#         url = reverse('book-detail', args=[99999])
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     # ----- Тесты для обновления книги (PUT /books/{id}/) -----
#     def test_update_book_full_authenticated(self):
#         """Тест: полное обновление книги (PUT)"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Война и мир (новая редакция)",
#             "author": self.author.id,
#             "isbn": "9785170909052",  # Тот же ISBN
#             "genre": "FICTION",
#             "publication_year": 1873,
#             "publisher": "Новое издательство",
#             "description": "Обновленное описание",
#             "total_copies": 10,
#             "available_copies": 8
#         }
#
#         response = self.client.put(self.detail_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.book.refresh_from_db()
#         self.assertEqual(self.book.title, "Война и мир (новая редакция)")
#         self.assertEqual(self.book.publication_year, 1873)
#         self.assertEqual(self.book.publisher, "Новое издательство")
#         self.assertEqual(self.book.description, "Обновленное описание")
#         self.assertEqual(self.book.total_copies, 10)
#         self.assertEqual(self.book.available_copies, 8)
#
#     def test_update_book_partial_authenticated(self):
#         """Тест: частичное обновление книги (PATCH)"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {
#             "title": "Война и мир (обновленное название)",
#             "available_copies": 3
#         }
#
#         response = self.client.patch(self.detail_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.book.refresh_from_db()
#         self.assertEqual(self.book.title, "Война и мир (обновленное название)")
#         self.assertEqual(self.book.available_copies, 3)
#         self.assertEqual(self.book.publication_year, 1869)  # Не изменилось
#         self.assertEqual(self.book.total_copies, 5)  # Не изменилось
#
#     def test_update_book_unauthenticated(self):
#         """Тест: обновление книги без авторизации (запрещено)"""
#         data = {"title": "Обновленное название"}
#
#         response = self.client.patch(self.detail_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.book.refresh_from_db()
#         self.assertEqual(self.book.title, "Война и мир")  # Не изменилось
#
#     def test_update_book_with_duplicate_isbn(self):
#         """Тест: обновление книги с ISBN другой книги"""
#         self.client.force_authenticate(user=self.user)
#
#         # Создаем другую книгу
#         other_book = Book.objects.create(
#             title="Другая книга",
#             author=self.author,
#             isbn="9785170909999",
#             publication_year=2000
#         )
#
#         data = {"isbn": other_book.isbn}
#
#         response = self.client.patch(self.detail_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("isbn", response.data)
#
#     def test_update_book_with_nonexistent_author(self):
#         """Тест: обновление книги с несуществующим автором"""
#         self.client.force_authenticate(user=self.user)
#
#         data = {"author": 99999}
#
#         response = self.client.patch(self.detail_url, data, format='json')
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertIn("author", response.data)
#
#     def test_update_nonexistent_book(self):
#         """Тест: обновление несуществующей книги"""
#         self.client.force_authenticate(user=self.user)
#         url = reverse('book-detail', args=[99999])
#
#         data = {"title": "Тест"}
#
#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     # ----- Тесты для удаления книги (DELETE /books/{id}/) -----
#     def test_delete_book_authenticated(self):
#         """Тест: удаление книги авторизованным пользователем"""
#         self.client.force_authenticate(user=self.user)
#
#         response = self.client.delete(self.detail_url)
#
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Book.objects.count(), 0)
#
#     def test_delete_book_unauthenticated(self):
#         """Тест: удаление книги без авторизации (запрещено)"""
#         response = self.client.delete(self.detail_url)
#
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(Book.objects.count(), 1)  # Книга не удалена
#
#     def test_delete_nonexistent_book(self):
#         """Тест: удаление несуществующей книги"""
#         self.client.force_authenticate(user=self.user)
#         url = reverse('book-detail', args=[99999])
#
#         response = self.client.delete(url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     # ----- Тесты для дополнительных методов -----
#     def test_book_is_available_field_in_response(self):
#         """Тест: поле is_available должно быть в ответе (если есть в сериализаторе)"""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.detail_url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Если сериализатор добавляет поле is_available
#         if 'is_available' in response.data:
#             self.assertTrue(response.data['is_available'])
#
#         # Проверяем список
#         list_response = self.client.get(self.list_url)
#         if list_response.status_code == status.HTTP_200_OK:
#             if list_response.data and 'is_available' in list_response.data[0]:
#                 self.assertTrue(list_response.data[0]['is_available'])
#
#     def test_author_details_in_book_response(self):
#         """Тест: в ответе должны быть детали автора (если сериализатор вложенный)"""
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.detail_url)
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Если сериализатор показывает автора в виде объекта
#         if isinstance(response.data.get('author'), dict):
#             self.assertEqual(response.data['author']['id'], self.author.id)
#             self.assertEqual(response.data['author']['first_name'], "Лев")
#             self.assertEqual(response.data['author']['last_name'], "Толстой")
#
#     # ----- Тесты прав доступа (IsAuthenticatedOrReadOnly) -----
#     def test_permissions_read_only_unauthenticated(self):
#         """Тест: неавторизованный пользователь может только читать"""
#         # GET - разрешено
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         response = self.client.get(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # POST - запрещено
#         data = {"title": "Тест", "author": self.author.id, "isbn": "123", "publication_year": 2000}
#         response = self.client.post(self.list_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#         # PUT - запрещено
#         response = self.client.put(self.detail_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#         # PATCH - запрещено
#         response = self.client.patch(self.detail_url, {"title": "Новое"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#         # DELETE - запрещено
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_permissions_write_authenticated(self):
#         """Тест: авторизованный пользователь может все операции"""
#         self.client.force_authenticate(user=self.user)
#
#         # GET - разрешено
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # POST - разрешено
#         data = {"title": "Новая книга", "author": self.author.id, "isbn": "9785170909998", "publication_year": 2000}
#         response = self.client.post(self.list_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # PATCH - разрешено
#         response = self.client.patch(self.detail_url, {"title": "Обновлено"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # DELETE - разрешено
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#
# class BookPermissionsTest(TestCase):
#     """Тесты прав доступа для разных ролей"""
#
#     def setUp(self):
#         self.client = APIClient()
#         self.author = Author.objects.create(
#             first_name="Лев",
#             last_name="Толстой"
#         )
#         self.book = Book.objects.create(
#             title="Тестовая книга",
#             author=self.author,
#             isbn="9785170900001",
#             publication_year=2000
#         )
#         self.list_url = reverse('book-list')
#         self.detail_url = reverse('book-detail', args=[self.book.id])
#
#     def test_admin_can_do_everything(self):
#         """Тест: администратор может делать все"""
#         admin = User.objects.create_superuser(
#             username="admin",
#             password="admin123",
#             email="admin@test.com"
#         )
#         self.client.force_authenticate(user=admin)
#
#         # GET
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # POST
#         data = {
#             "title": "Новая книга",
#             "author": self.author.id,
#             "isbn": "9785170900002",
#             "publication_year": 2000
#         }
#         response = self.client.post(self.list_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # PATCH
#         response = self.client.patch(self.detail_url, {"title": "Обновлено"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # DELETE
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def test_regular_user_can_write(self):
#         """Тест: обычный пользователь может писать (IsAuthenticatedOrReadOnly)"""
#         user = User.objects.create_user(
#             username="user",
#             password="user123"
#         )
#         self.client.force_authenticate(user=user)
#
#         # POST - разрешено
#         data = {
#             "title": "Новая книга",
#             "author": self.author.id,
#             "isbn": "9785170900003",
#             "publication_year": 2000
#         }
#         response = self.client.post(self.list_url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # PATCH - разрешено
#         response = self.client.patch(self.detail_url, {"title": "Обновлено"}, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # DELETE - разрешено
#         response = self.client.delete(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)