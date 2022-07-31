from rest_framework import serializers

from store.models import Product

class ProductSerializer(serializers.ModelSerializer):
    is_on_sale=serializers.BooleanField(read_only=True)
    current_price=serializers.FloatField(read_only=True)
    # renaming the fields
    # product_name = serializers.CharField(source='name')
    description=serializers.CharField(min_length=2, max_length=200)


    class Meta:
        model=Product
        fields=(
            "id",
            "name", #product_name,
            "description","price","sale_start","sale_end", 
            "is_on_sale", "current_price"
            )