from django_filters import FilterSet, DateFilter, DateRangeFilter

from .models import Post
from django import forms


class NewsFilter(FilterSet):
    start_date = DateFilter(field_name='date', lookup_expr=(
        'gt'), widget=forms.DateTimeInput(attrs={'type': 'date'}), label='от')
    end_date = DateFilter(field_name='date', lookup_expr=(
        'lt'), widget=forms.DateTimeInput(attrs={'type': 'date'}), label='до')
    date = DateRangeFilter(label='Дата')

    class Meta:
        model = Post
        fields = [
            'author',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(NewsFilter, self).__init__(*args, **kwargs)
        self.filters['author'].label = "Автор"
