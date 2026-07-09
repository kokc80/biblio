import pytest
from django.contrib.auth.models import User

from apps.authors.models import Author
from apps.books.models import Book


@pytest.fixture
def test_author():
    return Author.objects.create(
        name="Тестовый автор",
        birth_year=1990,
        country="Тестландия"
    )


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="testuser",
        password="testpass123"
    )


@pytest.fixture
def test_book(test_author):
    return Book.objects.create(
        title="Тестовая книга",
        author=test_author,
        is_available=True
    )
