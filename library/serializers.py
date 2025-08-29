from rest_framework import serializers
from .models import Book, Transaction

class BookSerializer(serializers.ModelSerializer):
    published_date = serializers.DateField(required=False, allow_null=True)
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "published_date", "copies_available"]

class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'status', 'borrow_date', 'return_date']
        read_only_fields = fields

# For creating a borrow (checkout): we only need a book id
class BorrowCreateSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate(self, attrs):
        # optional place for extra validation; view handles business logic.
        return attrs
