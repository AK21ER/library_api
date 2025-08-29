import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    available = django_filters.BooleanFilter(method="filter_available")

    class Meta:
        model = Book
        fields = ["title", "author", "isbn"]

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(copies_available__gt=0)
        return queryset
