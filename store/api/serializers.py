from rest_framework import serializers
from store.models import Product


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ["title", "brand", "model", "stock", "price", 'category', "slug"]