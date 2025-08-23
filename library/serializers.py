from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Book, Transaction, Borrow
from django.contrib.auth.models import User

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'copies_available']
class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
  book = BookSerializer(read_only=True)


  class Meta:
    model = Transaction
    fields = ['id', 'book', 'status', 'checkout_date', 'return_date']
    read_only_fields = fields


# Users API (CRUD) using built-in User
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    date_of_membership = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'date_of_membership', 'password']
        extra_kwargs = {
        'email': {'required': True},
        }


    def get_date_of_membership(self, obj):
    # Use date_joined as membership date
        return obj.date_joined.date() if obj.date_joined else None


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        validate_password(password, user)
        user.set_password(password)
        user.save()
        return user


def update(self, instance, validated_data):
    password = validated_data.pop('password', None)
    for attr, value in validated_data.items():
     setattr(instance, attr, value)
    if password:
     validate_password(password, instance)
     instance.set_password(password)
    instance.save()
    return instance

