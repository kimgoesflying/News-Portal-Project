from django_filters import FilterSet, DateFilter, DateRangeFilter, ModelMultipleChoiceFilter

from .models import Post, Category
from django import forms


class NewsFilter(FilterSet):

    start_date = DateFilter(field_name='date', lookup_expr=(
        'gt'), widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}), label='от')

    end_date = DateFilter(field_name='date', lookup_expr=(
        'lt'), widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}), label='до')

    date = DateRangeFilter(label='Дата', widget=forms.Select(
        attrs={'class': 'form-control'}))

    category = ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                         widget=forms.CheckboxSelectMultiple(),  label='Категории')

    class Meta:
        model = Post

        fields = [
            'category',
            'author',
            'date',
        ]

    def __init__(self, *args, **kwargs):
        super(NewsFilter, self).__init__(*args, **kwargs)
        self.filters['author'].label = "Автор"
        self.filters['author'].field.widget.attrs.update(
            {'class': 'form-control'})
