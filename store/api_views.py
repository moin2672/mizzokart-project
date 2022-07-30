from rest_framework.generics import ListAPIView

from store.serializers import ProductSerializer
from store.models import Product

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class ProductList(ListAPIView):
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=(DjangoFilterBackend,SearchFilter)
    filterset_fields = ('id', )  #note dont use filter_fields
    search_fields = ('name', 'description')

    def get_queryset(self):
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        queryset =  Product.objects.all()
        if on_sale.lower()=='true':
            from django.utils import timezone
            now = timezone.now()
            return queryset.filter(
                sale_start__lte= now,
                sale_end__gte=now,
            )
        return queryset
