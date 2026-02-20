from rest_framework import serializers
from .models import Book # type: ignore

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
