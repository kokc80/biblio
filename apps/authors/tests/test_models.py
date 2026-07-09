from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from datetime import date
from apps.authors.models import Author


class AuthorModelTest(TestCase):
    """Тесты для модели Author"""

    def setUp(self):
        """Создание тестовых данных перед каждым тестом"""
        self.author_data = {
            "first_name": "Лев",
            "last_name": "Толстой",
            "birth_date": date(1828, 9, 9),
            "biography": "Великий русский писатель"
        }
        self.author = Author.objects.create(**self.author_data)

    # ----- Тесты создания -----
    def test_create_author(self):
        """Тест создания автора с полными данными"""
        author = Author.objects.create(
            first_name="Фёдор",
            last_name="Достоевский",
            birth_date=date(1821, 11, 11),
            biography="Русский писатель, мыслитель"
        )

        self.assertEqual(author.first_name, "Фёдор")
        self.assertEqual(author.last_name, "Достоевский")
        self.assertEqual(author.birth_date, date(1821, 11, 11))
        self.assertEqual(author.biography, "Русский писатель, мыслитель")
        self.assertIsNotNone(author.id)
        self.assertIsNotNone(author.created_at)
        self.assertIsNotNone(author.updated_at)

    def test_create_author_minimal_data(self):
        """Тест создания автора только с обязательными полями"""
        author = Author.objects.create(
            first_name="Александр",
            last_name="Пушкин"
        )

        self.assertEqual(author.first_name, "Александр")
        self.assertEqual(author.last_name, "Пушкин")
        self.assertIsNone(author.birth_date)
        self.assertEqual(author.biography, "")

    def test_create_author_without_first_name_should_fail(self):
        """Тест: создание автора без имени должно вызвать ошибку"""
        with self.assertRaises(IntegrityError):
            Author.objects.create(
                first_name=None,  # недопустимо
                last_name="Толстой"
            )

    def test_create_author_without_last_name_should_fail(self):
        """Тест: создание автора без фамилии должно вызвать ошибку"""
        with self.assertRaises(IntegrityError):
            Author.objects.create(
                first_name="Лев",
                last_name=None  # недопустимо
            )

    # ----- Тесты строкового представления -----
    def test_str_method(self):
        """Тест метода __str__"""
        author = Author(first_name="Иван", last_name="Тургенев")
        self.assertEqual(str(author), "Иван Тургенев")

    def test_str_method_with_empty_first_name(self):
        """Тест __str__ если имя пустое (хотя такого быть не должно)"""
        author = Author(first_name="", last_name="Толстой")
        self.assertEqual(str(author), " Толстой")  # пробел в начале

    # ----- Тесты полей -----
    def test_birth_date_optional(self):
        """Тест: дата рождения опциональна"""
        author = Author.objects.create(
            first_name="Джордж",
            last_name="Оруэлл"
        )
        self.assertIsNone(author.birth_date)

    def test_biography_optional(self):
        """Тест: биография опциональна и может быть пустой"""
        author = Author.objects.create(
            first_name="Тест",
            last_name="Тестов"
        )
        self.assertEqual(author.biography, "")
        self.assertEqual(author.biography, "")  # default blank=True

    def test_biography_long_text(self):
        """Тест: биография может содержать длинный текст"""
        long_biography = "A" * 1000
        author = Author.objects.create(
            first_name="Тест",
            last_name="Тестов",
            biography=long_biography
        )
        self.assertEqual(len(author.biography), 1000)

    # ----- Тесты автоматических полей -----
    def test_created_at_auto_now_add(self):
        """Тест: created_at устанавливается автоматически при создании"""
        self.assertIsNotNone(self.author.created_at)
        # Проверяем, что время создания близко к текущему
        time_diff = timezone.now() - self.author.created_at
        self.assertLess(time_diff.total_seconds(), 5)  # меньше 5 секунд

    def test_updated_at_auto_now(self):
        """Тест: updated_at обновляется при сохранении"""
        old_updated_at = self.author.updated_at

        # Ждем немного и обновляем
        import time
        time.sleep(1)

        self.author.biography = "Обновленная биография"
        self.author.save()
        self.author.refresh_from_db()

        # updated_at должно измениться
        self.assertNotEqual(self.author.updated_at, old_updated_at)
        self.assertGreater(self.author.updated_at, old_updated_at)

    def test_created_at_does_not_change_on_update(self):
        """Тест: created_at НЕ меняется при обновлении"""
        old_created_at = self.author.created_at

        self.author.biography = "Новая биография"
        self.author.save()
        self.author.refresh_from_db()

        self.assertEqual(self.author.created_at, old_created_at)

    # ----- Тесты упорядочивания (Meta.ordering) -----
    def test_ordering_by_last_name_then_first_name(self):
        """Тест: авторы сортируются по фамилии, затем по имени"""
        # Создаем авторов в разном порядке
        Author.objects.create(first_name="Антон", last_name="Чехов")
        Author.objects.create(first_name="Иван", last_name="Бунин")
        Author.objects.create(first_name="Фёдор", last_name="Достоевский")

        authors = Author.objects.all()

        # Проверяем порядок: Бунин, Достоевский, Толстой, Чехов
        self.assertEqual(authors[0].last_name, "Бунин")
        self.assertEqual(authors[1].last_name, "Достоевский")
        self.assertEqual(authors[2].last_name, "Толстой")
        self.assertEqual(authors[3].last_name, "Чехов")

    def test_ordering_with_same_last_name(self):
        """Тест: при одинаковой фамилии сортировка по имени"""
        Author.objects.create(first_name="Анна", last_name="Толстая")
        Author.objects.create(first_name="Лев", last_name="Толстой")
        Author.objects.create(first_name="Алексей", last_name="Толстой")

        # Получаем всех Толстых
        authors = Author.objects.filter(last_name="Толстой")

        # Проверяем, что сортировка по имени (Алексей, Лев)
        self.assertEqual(authors[0].first_name, "Алексей")
        self.assertEqual(authors[1].first_name, "Лев")

    # ----- Тесты методов модели -----
    def test_get_full_name(self):
        """Тест метода получения полного имени (если есть)"""
        # Если у тебя есть метод get_full_name, раскомментируй:
        # self.assertEqual(self.author.get_full_name(), "Лев Толстой")
        pass

    def test_author_age_calculation(self):
        """Тест расчета возраста (если есть метод)"""
        # Если у тебя есть метод get_age, раскомментируй:
        # age = self.author.get_age()
        # self.assertEqual(age, 2026 - 1828)  # или что-то подобное
        pass

    # ----- Тесты QuerySet -----
    def test_filter_by_name(self):
        """Тест поиска авторов по имени"""
        authors = Author.objects.filter(first_name="Лев")
        self.assertEqual(authors.count(), 1)
        self.assertEqual(authors[0].last_name, "Толстой")

    def test_filter_by_last_name(self):
        """Тест поиска авторов по фамилии"""
        # Создаем еще одного Толстого
        Author.objects.create(first_name="Алексей", last_name="Толстой")

        authors = Author.objects.filter(last_name="Толстой")
        self.assertEqual(authors.count(), 2)

    def test_filter_by_birth_year(self):
        """Тест поиска по году рождения"""
        # Создаем автора
        Author.objects.create(
            first_name="Фёдор",
            last_name="Достоевский",
            birth_date=date(1821, 11, 11)
        )

        # Ищем всех, кто родился в 1821 году
        authors = Author.objects.filter(birth_date__year=1821)
        self.assertEqual(authors.count(), 1)
        self.assertEqual(authors[0].last_name, "Достоевский")

    def test_search_by_biography(self):
        """Тест поиска по тексту биографии"""
        Author.objects.create(
            first_name="Антон",
            last_name="Чехов",
            biography="Великий русский писатель и драматург"
        )

        # Ищем по ключевому слову в биографии
        authors = Author.objects.filter(biography__icontains="драматург")
        self.assertEqual(authors.count(), 1)
        self.assertEqual(authors[0].last_name, "Чехов")

    # ----- Тесты обновления -----
    def test_update_author(self):
        """Тест обновления данных автора"""
        self.author.first_name = "Лев Николаевич"
        self.author.biography = "Великий русский писатель, мыслитель"
        self.author.save()
        self.author.refresh_from_db()

        self.assertEqual(self.author.first_name, "Лев Николаевич")
        self.assertEqual(self.author.biography, "Великий русский писатель, мыслитель")

    def test_update_only_one_field(self):
        """Тест обновления только одного поля"""
        old_biography = self.author.biography
        old_first_name = self.author.first_name

        self.author.last_name = "Толстой-Граф"
        self.author.save()
        self.author.refresh_from_db()

        self.assertEqual(self.author.last_name, "Толстой-Граф")
        self.assertEqual(self.author.first_name, old_first_name)
        self.assertEqual(self.author.biography, old_biography)

    # ----- Тесты удаления -----
    def test_delete_author(self):
        """Тест удаления автора"""
        author_id = self.author.id
        self.author.delete()

        with self.assertRaises(Author.DoesNotExist):
            Author.objects.get(id=author_id)

    def test_cascade_delete(self):
        """Тест каскадного удаления (если есть связанные модели)"""
        # Если есть связанные книги, проверяем, что они удаляются
        # Или что защищено от удаления
        pass