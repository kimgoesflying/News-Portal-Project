from django_filters import FilterSet, DateFilter, DateRangeFilter, ModelChoiceFilter

from .models import Post, Author
from django import forms


class NewsFilter(FilterSet):

    start_date = DateFilter(field_name='date', lookup_expr=(
        'gt'), widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}), label='от')

    end_date = DateFilter(field_name='date', lookup_expr=(
        'lt'), widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}), label='до')

    date = DateRangeFilter(label='Дата', widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = [
            'author',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(NewsFilter, self).__init__(*args, **kwargs)
        self.filters['author'].label = "Автор"
        self.filters['author'].field.widget.attrs.update(
            {'class': 'form-control'})

        # print(self.filters['author'].field)
