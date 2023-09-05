from rest_framework import serializers
from .models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
