from .models import Author, Book
from rest_framework import serializers

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    # books = BookSerializer(many=True)
    books = serializers.StringRelatedField(many=True)
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'bio', 'books']

class BookSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField()
    genre = serializers.StringRelatedField(many=True)
    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'author', 'genre']
