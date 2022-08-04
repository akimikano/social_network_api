from django_filters import rest_framework as filters
from apps.main.models import Analytic


class AnalyticFilter(filters.FilterSet):
    post = filters.NumberFilter(field_name='post', required=True)
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_until = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Analytic
        fields = ('date_from', 'date_until',)
