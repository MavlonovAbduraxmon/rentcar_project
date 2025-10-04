from django_filters import FilterSet, NumberFilter

from apps.models import Car


class CarFilter(FilterSet):
    min_price = NumberFilter(field_name="price_per_day", lookup_expr="gte")
    max_price = NumberFilter(field_name="price_per_day", lookup_expr="lte")

    class Meta:
        model = Car
        fields = ["category", "brand", "fuel_type"]
