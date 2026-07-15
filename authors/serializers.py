from rest_framework import serializers

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "birth_date",
            "biography",
            "book_count",
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_book_count(self, obj):
        return obj.books.count()
