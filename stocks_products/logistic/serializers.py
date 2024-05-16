from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

    def create(self, validated_data):
        Prod = super().create(validated_data)
        return Prod


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']

    def create(self, validated_data):
        ProductPos = super().create(validated_data)
        return ProductPos


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    positions = ProductPositionSerializer(many=True)

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position_data in positions:
            StockProduct.objects.create(stock=stock,
                                        **position_data)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position_data in positions:
            StockProduct.objects.update_or_create(stock=stock,
                                                  defaults={
                                                      'quantity': position_data['quantity'],
                                                      'price': position_data['price']
                                                  },
                                                  product=position_data['product'])

        return stock
