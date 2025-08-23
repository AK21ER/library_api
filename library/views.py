from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer
from accounts.models import CustomUser
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Books CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    # Filter available books
    def get_queryset(self):
        queryset = Book.objects.all()
        available = self.request.query_params.get("available")
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        isbn = self.request.query_params.get("isbn")
        if available == "true":
            queryset = queryset.filter(available_copies__gt=0)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if isbn:
            queryset = queryset.filter(isbn=isbn)
        return queryset

# Users CRUD
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# Borrow / Checkout / Return
class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    @action(detail=True, methods=["post"])
    def checkout(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        user_id = request.data.get("user_id")
        user = get_object_or_404(CustomUser, pk=user_id)

        # Check if copies available
        if book.available_copies < 1:
            return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already borrowed
        if Borrow.objects.filter(book=book, borrower_name=user.username, status="OUT").exists():
            return Response({"error": "User already borrowed this book"}, status=status.HTTP_400_BAD_REQUEST)

        borrow = Borrow.objects.create(
            book=book,
            borrower_name=user.username,
            borrow_date=timezone.now(),
            status="OUT"
        )
        book.available_copies -= 1
        book.save()
        serializer = BorrowSerializer(borrow)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def return_book(self, request, pk=None):
        borrow = get_object_or_404(Borrow, pk=pk)
        if borrow.status != "OUT":
            return Response({"error": "Book is not checked out"}, status=status.HTTP_400_BAD_REQUEST)
        borrow.status = "AVL"
        borrow.return_date = timezone.now()
        borrow.save()
        book = borrow.book
        book.available_copies += 1
        book.save()
        serializer = BorrowSerializer(borrow)
        return Response(serializer.data)
