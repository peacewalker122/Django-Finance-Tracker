import django_filters
from django import forms
from tracker.models import Transaction, Category


class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_CHOICES,
        field_name='type',
        lookup_expr='iexact',
        empty_label='Any'
    )

    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='Start Date',
        widget=forms.DateInput(attrs={'type':'date'})
    )

    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='End Date',
        widget=forms.DateInput(attrs={'type':'date'})
    )

    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'start_date', 'end_date', 'categories']