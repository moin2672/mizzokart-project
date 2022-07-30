from rest_framework.generics import ListAPIView, CreateAPIView

from store.serializers import ProductSerializer
from store.models import Product

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from rest_framework.pagination import LimitOffsetPagination

from rest_framework.exceptions import ValidationError

class ProductsPagination(LimitOffsetPagination):
    default_limit=10
    max_limit=100

class ProductList(ListAPIView):
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=(DjangoFilterBackend,SearchFilter)
    filterset_fields = ('id', )  #note dont use filter_fields
    search_fields = ('name', 'description')
    pagination_class = ProductsPagination


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


class ProductCreate(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class=ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price)<=0.0:
                raise ValidationError({'price' : 'Must be above $0.00'})
        except ValueError:
            raise ValidationError({'price':'A valid number is required'})

        return super().create(request,  *args, **kwargs)