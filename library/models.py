from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


from django.core.validators import MinValueValidator



STATUS_CHOICES = [
    ("AVL", "Available"),
    ("OUT", "Checked Out"),
]


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])


class Meta:
    ordering = ["title"]


def __str__(self):
    return f"{self.title} by {self.author}"


class Transaction(models.Model):
    OUT = "out"
    IN = "in"

    STATUS_CHOICES = [
        (OUT, "Checked out"),
        (IN, "Returned"),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=[(IN, "Returned"), (OUT, "Borrowed")])
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)



class Meta:
    ordering = ['-checkout_date']
    indexes = [
    models.Index(fields=['user', 'book', 'status']),
    ]


def __str__(self):
    return f"{self.user} → {self.book} ({self.status})"

# class Borrow(models.Model):
#     book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrows")
#     borrower_name = models.CharField(max_length=255)
#     borrow_date = models.DateTimeField(null=True, blank=True)
#     return_date = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=3, choices=STATUS_CHOICES, default="AVL")

#     def __str__(self):
#         return f"{self.borrower_name} - {self.book.title}"