import django_filters
from . models import *
from django_filters import CharFilter,NumberFilter


class BookFilter(django_filters.FilterSet):
    # a filter which checks if entered characters are in any of the titles of the books
    title = CharFilter(field_name='title',lookup_expr='icontains')
    author = CharFilter(field_name='author',lookup_expr='icontains')
    publication=NumberFilter(field_name='yearOfPublication', lookup_expr='lt')
    class Meta:
        model=Book
        fields='__all__'
        exclude=['copies','date_created','description','tags','yearOfPublication']