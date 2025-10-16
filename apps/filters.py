from django_filters import FilterSet, NumberFilter, CharFilter

from apps.models import Car


class CarFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    categoty_id = CharFilter(field_name='category__id', lookup_expr='cars')
    brand_id = CharFilter(field_name='brand__brand_id', lookup_expr='cars')

    class Meta:
        model = Car
        fields = ['category_id', 'brand_id','fuel_type']
