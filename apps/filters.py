from django_filters import CharFilter, FilterSet, NumberFilter

from apps.models import Car


class CarFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    categoty_id = CharFilter(field_name='category__name', lookup_expr='icontains')
    brand_id = CharFilter(field_name='brand__brand_name', lookup_expr='icontains')

    class Meta:
        model = Car
        fields = ['name', 'category_id', 'brand_id', 'fuel_type', 'is_available']
