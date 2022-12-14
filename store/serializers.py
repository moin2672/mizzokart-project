from itertools import product
from rest_framework import serializers

from store.models import Product, ShoppingCartItem

class CartItemSerializer(serializers.ModelSerializer):
    quantity=serializers.IntegerField(min_value=1, max_value=100)
    class Meta:
        model = ShoppingCartItem
        fields=('product', 'quantity')

class ProductSerializer(serializers.ModelSerializer):
    is_on_sale=serializers.BooleanField(read_only=True)
    current_price=serializers.FloatField(read_only=True)
    # renaming the fields
    # product_name = serializers.CharField(source='name')
    description=serializers.CharField(min_length=2, max_length=2000)
    cart_items = serializers.SerializerMethodField() # by default call method get_CartItems()
    price=serializers.FloatField(
        min_value=1.00, max_value=100000.00,
        )
    # price=serializers.DecimalField(
    #     min_value=1.00, max_value=100000,
    #     max_digits=None, decimal_places=2,
    # )
    

    class Meta:
        model=Product
        fields=(
            "id",
            "name", #product_name,
            "description","price","sale_start","sale_end", 
            "is_on_sale", "current_price",
            "cart_items",
            )

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data  #many=True to serialize a collection of items