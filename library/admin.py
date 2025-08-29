from django.contrib import admin
from .models import Book, Transaction

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "published_date", "copies_available")
    search_fields = ("title", "author", "isbn")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "book", "borrow_date", "return_date"]
    list_filter = ("status",)
    search_fields = ("user__username", "book__title", "book__isbn")
