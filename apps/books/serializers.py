from rest_framework import serializers
from .models import Book
from apps.authors.models import Author


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "author_name",
            "author_id",
            "isbn",
            "genre",
            "publication_year",
            "publisher",
            "description",
            "total_copies",
            "available_copies",
        ]

    def get_author_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"
