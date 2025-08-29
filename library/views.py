from django.db import transaction as db_tx
from django.utils import timezone
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Book, Transaction
from .serializers import (
    BookSerializer,
    TransactionSerializer,
    BorrowCreateSerializer,
)
from .permissions import IsAdminOrReadOnly
from .filters import BookFilter

# Books CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated & IsAdminOrReadOnly]
    filterset_class = BookFilter
    search_fields = ["title", "author", "isbn"]
    ordering_fields = ["title", "author", "published_date", "copies_available"]

# Transactions list (read-only). Users see own; admins see all
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = Transaction.objects.select_related("book", "user")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

# Borrows endpoint that matches README:
# POST /api/borrows/ -> checkout
# PUT  /api/borrows/{id}/ -> return (close) a borrow
class BorrowViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.select_related("book", "user")

    def get_serializer_class(self):
        if self.action == "create":
            return BorrowCreateSerializer
        return TransactionSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if not request.user.is_staff:
            qs = qs.filter(user=request.user)
        page = self.paginate_queryset(qs)
        ser = TransactionSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(ser.data)
        return Response(ser.data)

    # Checkout
    def create(self, request, *args, **kwargs):
        ser = BorrowCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        book_id = ser.validated_data["book_id"]

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Book not found."}, status=404)

        user = request.user

        with db_tx.atomic():
            # lock the row to avoid race conditions
            book = Book.objects.select_for_update().get(pk=book.pk)

            if book.copies_available <= 0:
                return Response({"detail": "No copies available."}, status=400)

            if Transaction.objects.filter(user=user, book=book, status=Transaction.OUT).exists():
                return Response({"detail": "Already checked out."}, status=400)

            tx = Transaction.objects.create(user=user, book=book, status=Transaction.OUT)
            book.copies_available -= 1
            book.save(update_fields=["copies_available"])

        return Response(TransactionSerializer(tx).data, status=201)

    # Return (close) a borrow
    def update(self, request, *args, **kwargs):
        try:
            tx = Transaction.objects.select_related("book").get(pk=kwargs["pk"])
        except Transaction.DoesNotExist:
            return Response({"detail": "Borrow not found."}, status=404)

        # Only owner or admin can return
        if not (request.user.is_staff or tx.user == request.user):
            return Response({"detail": "Not allowed."}, status=403)

        if tx.status == Transaction.IN:
            return Response({"detail": "Already returned."}, status=400)

        with db_tx.atomic():
            book = Book.objects.select_for_update().get(pk=tx.book_id)
            tx.status = Transaction.IN
            tx.return_date = timezone.now()
            tx.save(update_fields=["status", "return_date"])

            book.copies_available += 1
            book.save(update_fields=["copies_available"])

        return Response(TransactionSerializer(tx).data, status=200)
